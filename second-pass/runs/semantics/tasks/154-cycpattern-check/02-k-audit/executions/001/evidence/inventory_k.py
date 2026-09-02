#!/usr/bin/env python3
"""Produce a source-linked inventory of every local K sentence in audit scope."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
CANDIDATE_ROOT = Path("/candidate")
OUTPUT = Path("/audit-output/evidence/k_rule_inventory.md")

FILES = [
    SEMANTICS_ROOT / "semantics.k",
    *sorted((SEMANTICS_ROOT / "semantics").glob("*.k")),
    CANDIDATE_ROOT / "verification.k",
    CANDIDATE_ROOT / "spec.k",
]

START = re.compile(
    r"^(?P<indent> {0,2})(?P<kind>"
    r"requires|module|endmodule|imports|configuration|syntax|context|rule|claim"
    r")\b"
)
ATTRIBUTE_NAMES = [
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "owise",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]


def relpath(path: Path) -> str:
    if path.is_relative_to(SEMANTICS_ROOT):
        return "trusted-reference-semantics/" + str(path.relative_to(SEMANTICS_ROOT))
    return "candidate/" + path.name


def find_sentences(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))

    for ordinal, (start, kind) in enumerate(starts, 1):
        raw_end = starts[ordinal][0] if ordinal < len(starts) else len(lines)
        end = raw_end
        while end > start + 1 and (
            not lines[end - 1].strip()
            or lines[end - 1].lstrip().startswith("//")
        ):
            end -= 1
        text = "\n".join(lines[start:end]).rstrip()
        yield {
            "ordinal": ordinal,
            "kind": kind,
            "start": start + 1,
            "end": end,
            "text": text,
        }


def attributes(text: str) -> list[str]:
    found = []
    for attribute in ATTRIBUTE_NAMES:
        if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(attribute)}(?![A-Za-z0-9_-])", text):
            found.append(attribute)
    return found


def classification(kind: str, attrs: list[str]) -> str:
    if kind != "rule":
        if kind == "syntax" and "no-evaluators" in attrs:
            return "opaque-symbol-declaration"
        if kind == "syntax":
            return "syntax-declaration"
        return kind
    if "simplification" in attrs:
        return "simplification-rule"
    if "concrete" in attrs:
        return "concrete-only-rule"
    return "ordinary-rule"


def main() -> int:
    output_lines = [
        "# Exhaustive K sentence and rule inventory",
        "",
        "Generated directly from the trusted supplied-semantics tree and the "
        "candidate proof/spec sources. Each record contains the complete source "
        "sentence, so multiline guards, cell footprints, and attributes remain visible.",
        "",
    ]
    global_kinds = collections.Counter()
    global_classes = collections.Counter()
    global_attributes = collections.Counter()

    for path in FILES:
        file_text = path.read_bytes()
        sentences = list(find_sentences(path))
        file_kinds = collections.Counter(item["kind"] for item in sentences)
        file_classes = collections.Counter()
        for item in sentences:
            attrs = attributes(item["text"])
            item["attributes"] = attrs
            item["class"] = classification(item["kind"], attrs)
            file_classes[item["class"]] += 1
            global_kinds[item["kind"]] += 1
            global_classes[item["class"]] += 1
            global_attributes.update(attrs)

        output_lines.extend(
            [
                f"## `{relpath(path)}`",
                "",
                f"- SHA-256: `{hashlib.sha256(file_text).hexdigest()}`",
                f"- Sentence counts: `{dict(sorted(file_kinds.items()))}`",
                f"- Classification counts: `{dict(sorted(file_classes.items()))}`",
                "",
            ]
        )
        for item in sentences:
            attr_text = ", ".join(item["attributes"]) or "none"
            output_lines.extend(
                [
                    f"### {item['ordinal']}. {item['kind']} "
                    f"(lines {item['start']}-{item['end']})",
                    "",
                    f"Class: `{item['class']}`. Attributes: `{attr_text}`.",
                    "",
                    "```k",
                    item["text"],
                    "```",
                    "",
                ]
            )

    output_lines.extend(
        [
            "## Global counts",
            "",
            f"- Sentence kinds: `{dict(sorted(global_kinds.items()))}`",
            f"- Classifications: `{dict(sorted(global_classes.items()))}`",
            f"- Attributes: `{dict(sorted(global_attributes.items()))}`",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(output_lines), encoding="utf-8")

    print(f"files={len(FILES)}")
    print(f"sentence_kinds={dict(sorted(global_kinds.items()))}")
    print(f"classifications={dict(sorted(global_classes.items()))}")
    print(f"attributes={dict(sorted(global_attributes.items()))}")
    print(f"inventory={OUTPUT}")
    print(f"inventory_sha256={hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
