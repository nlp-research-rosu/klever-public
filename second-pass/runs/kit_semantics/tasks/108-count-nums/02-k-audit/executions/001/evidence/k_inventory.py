#!/usr/bin/env python3
"""Lexically enumerate every K declaration used by the audit."""

from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


START_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>"
    r"syntax|rule|configuration|context|claim|alias"
    r")\b"
)
BOUNDARY_RE = re.compile(
    r"^[ \t]*(?:syntax|rule|configuration|context|claim|alias|endmodule)\b"
)
TRAILING_ATTRIBUTE_RE = re.compile(r"\[([^\[\]]*)\]\s*$", re.DOTALL)


@dataclass
class Sentence:
    path: Path
    line_start: int
    line_end: int
    kind: str
    text: str
    attributes: tuple[str, ...]


def mask_comments(text: str) -> str:
    result = list(text)
    state = "code"
    depth = 0
    index = 0
    while index < len(text):
        char = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if char == "\n":
                state = "code"
            else:
                result[index] = " "
            index += 1
            continue
        if state == "block":
            if char == "/" and following == "*":
                result[index] = result[index + 1] = " "
                depth += 1
                index += 2
            elif char == "*" and following == "/":
                result[index] = result[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
            else:
                if char != "\n":
                    result[index] = " "
                index += 1
            continue
        if state == "string":
            if char == "\\" and following:
                result[index] = result[index + 1] = " "
                index += 2
            elif char == '"':
                state = "code"
                index += 1
            else:
                if char != "\n":
                    result[index] = " "
                index += 1
            continue
        if char == "/" and following == "/":
            result[index] = result[index + 1] = " "
            state = "line"
            index += 2
        elif char == "/" and following == "*":
            result[index] = result[index + 1] = " "
            state = "block"
            depth = 1
            index += 2
        elif char == '"':
            state = "string"
            index += 1
        else:
            index += 1
    return "".join(result)


def attributes(text: str) -> tuple[str, ...]:
    result: list[str] = []
    match = TRAILING_ATTRIBUTE_RE.search(text)
    if match is not None:
        for token in match.group(1).split(","):
            stripped = token.strip()
            if stripped:
                result.append(stripped)
    return tuple(result)


def scan(path: Path) -> list[Sentence]:
    text = path.read_text()
    raw_lines = text.splitlines()
    masked_lines = mask_comments(text).splitlines()
    starts: list[tuple[int, str]] = []
    for index, masked in enumerate(masked_lines):
        match = START_RE.match(masked)
        if match:
            starts.append((index, match.group("kind")))
    result: list[Sentence] = []
    for number, (start, kind) in enumerate(starts):
        limit = starts[number + 1][0] if number + 1 < len(starts) else len(raw_lines)
        for index in range(start + 1, limit):
            if re.match(r"^[ \t]*endmodule\b", masked_lines[index]):
                limit = index
                break
        while limit > start and not raw_lines[limit - 1].strip():
            limit -= 1
        raw = "\n".join(raw_lines[start:limit]).strip()
        normalized = " ".join(raw.split())
        result.append(
            Sentence(
                path=path,
                line_start=start + 1,
                line_end=limit,
                kind=kind,
                text=normalized,
                attributes=attributes(raw),
            )
        )
    return result


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: k_inventory.py SEMANTICS_ROOT VERIFICATION.k OUTPUT.md",
            file=sys.stderr,
        )
        return 2
    semantics_root = Path(sys.argv[1])
    verification = Path(sys.argv[2])
    output = Path(sys.argv[3])
    spec = verification.with_name("spec.k")

    paths = sorted(semantics_root.rglob("*.k")) + [verification, spec]
    all_sentences: list[Sentence] = []
    file_hashes: dict[str, str] = {}
    for path in paths:
        all_sentences.extend(scan(path))
        file_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()

    kind_counts = collections.Counter(sentence.kind for sentence in all_sentences)
    attribute_counts: collections.Counter[str] = collections.Counter()
    for sentence in all_sentences:
        attribute_counts.update(sentence.attributes)

    special = {
        "function": [],
        "total": [],
        "functional": [],
        "no-evaluators": [],
        "simplification": [],
        "concrete": [],
        "symbolic": [],
        "priority": [],
        "owise": [],
    }
    for sentence in all_sentences:
        for key in special:
            if any(attr == key or attr.startswith(key + "(") for attr in sentence.attributes):
                special[key].append(
                    f"{sentence.path}:{sentence.line_start}-{sentence.line_end}"
                )

    lines = [
        "# Exhaustive K source inventory",
        "",
        "This is a lexical inventory of every `syntax`, `rule`, `configuration`, "
        "`context`, `claim`, and `alias` sentence in the trusted supplied "
        "semantics, candidate `verification.k`, and positive `spec.k`.",
        "",
        "## Summary",
        "",
        f"- Files: {len(paths)}",
        f"- Sentences: {len(all_sentences)}",
        f"- Kind counts: `{json.dumps(dict(sorted(kind_counts.items())), sort_keys=True)}`",
        f"- Attribute counts: `{json.dumps(dict(sorted(attribute_counts.items())), sort_keys=True)}`",
        "",
        "### Special attributes",
        "",
    ]
    for key, occurrences in special.items():
        lines.append(f"- `{key}` ({len(occurrences)}): " + ", ".join(occurrences))
    lines += ["", "## Per-file inventory", ""]

    for path in paths:
        provenance = (
            "candidate proof extension/claim"
            if path in {verification, spec}
            else "trusted supplied semantics"
        )
        lines += [
            f"### `{path}`",
            "",
            f"SHA-256: `{file_hashes[str(path)]}`. Provenance: {provenance}.",
            "",
        ]
        sentences = [sentence for sentence in all_sentences if sentence.path == path]
        if not sentences:
            lines += ["No inventoried sentence.", ""]
            continue
        for sentence in sentences:
            attr_text = (
                ", attributes: `" + "`, `".join(sentence.attributes) + "`"
                if sentence.attributes
                else ""
            )
            lines += [
                f"- Lines {sentence.line_start}-{sentence.line_end}; "
                f"kind `{sentence.kind}`{attr_text}: `{sentence.text}`"
            ]
        lines.append("")

    output.write_text("\n".join(lines))
    print(f"output={output}")
    print(f"files={len(paths)}")
    print(f"sentences={len(all_sentences)}")
    print(f"kind_counts={dict(sorted(kind_counts.items()))}")
    print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
    for key, occurrences in special.items():
        print(f"special[{key}]={len(occurrences)}")
    print("INVENTORY_COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
