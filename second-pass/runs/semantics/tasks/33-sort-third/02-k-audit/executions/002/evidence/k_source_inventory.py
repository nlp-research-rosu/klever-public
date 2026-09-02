#!/usr/bin/env python3
"""Create a complete lexical inventory of local K source sentences.

The inventory is intentionally source-oriented: every outer syntax,
configuration, context, rule, claim, alias, import, and module boundary is
recorded with source lines, normalized digest, attributes, and full text.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
HEAD = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>"
    r"requires|module|endmodule|imports|syntax|configuration|"
    r"context|rule|claim|alias"
    r")\b"
)
ATTR = re.compile(r"\[([^\[\]]*)\]", re.S)
KNOWN_ATTR = re.compile(
    r"(?<![A-Za-z0-9_-])("
    r"function|total|functional|simplification|owise|concrete|"
    r"macro-rec|macro|no-evaluators|"
    r"priority\(\d+\)|strict(?:\([^)]*\))?|seqstrict\([^)]*\)|"
    r"symbol\([^)]*\)"
    r")(?![A-Za-z0-9_-])"
)


def mask_comments(text: str) -> str:
    output = list(text)
    index = 0
    state = "code"
    depth = 0
    while index < len(text):
        here = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line":
            if here == "\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block":
            if here == "/" and following == "*":
                output[index] = output[index + 1] = " "
                depth += 1
                index += 2
                continue
            if here == "*" and following == "/":
                output[index] = output[index + 1] = " "
                depth -= 1
                index += 2
                if depth == 0:
                    state = "code"
                continue
            if here != "\n":
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if here == "\\" and following:
                index += 2
                continue
            if here == '"':
                state = "code"
            index += 1
            continue
        if here == "/" and following == "/":
            output[index] = output[index + 1] = " "
            state = "line"
            index += 2
            continue
        if here == "/" and following == "*":
            output[index] = output[index + 1] = " "
            state = "block"
            depth = 1
            index += 2
            continue
        if here == '"':
            state = "string"
        index += 1
    return "".join(output)


def sentence_starts(masked_lines: list[str]) -> list[tuple[int, str]]:
    starts: list[tuple[int, str]] = []
    in_rule = False
    for index, line in enumerate(masked_lines):
        match = HEAD.match(line)
        if match is None:
            continue
        kind = match.group("kind")
        indent = match.group("indent")
        # File-level requires is unindented. Indented requires belongs to a
        # preceding rule and therefore is not an outer sentence.
        if kind == "requires" and indent:
            continue
        if kind in {"rule", "claim", "context", "syntax", "configuration"}:
            in_rule = kind in {"rule", "claim"}
        elif kind not in {"requires"}:
            in_rule = False
        starts.append((index, kind))
    return starts


def attributes(text: str, kind: str) -> list[str]:
    found: list[str] = []
    for match in ATTR.finditer(mask_comments(text)):
        content = match.group(1).strip()
        found.extend(attribute.group(1) for attribute in KNOWN_ATTR.finditer(content))
        if kind == "claim" and re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", content):
            found.append(f"label({content})")
    return found


def main() -> None:
    documents: list[dict[str, object]] = []
    for path in ROOTS:
        raw = path.read_text(encoding="utf-8")
        lines = raw.splitlines(keepends=True)
        masked_lines = mask_comments(raw).splitlines(keepends=True)
        starts = sentence_starts(masked_lines)
        for ordinal, (start, kind) in enumerate(starts, 1):
            end = starts[ordinal][0] if ordinal < len(starts) else len(lines)
            text = "".join(lines[start:end]).rstrip()
            normalized = " ".join(mask_comments(text).split())
            attrs = attributes(text, kind)
            digest = hashlib.sha256(normalized.encode()).hexdigest()
            documents.append(
                {
                    "id": f"{path.name}:{start + 1}:{digest[:12]}",
                    "path": str(path),
                    "kind": kind,
                    "start_line": start + 1,
                    "end_line": end,
                    "attributes": attrs,
                    "classifications": {
                        "function": any(a == "function" for a in attrs),
                        "total": any(a == "total" for a in attrs),
                        "functional": any(a == "functional" for a in attrs),
                        "simplification": any(
                            a == "simplification" for a in attrs
                        ),
                        "priority": any(a.startswith("priority(") for a in attrs),
                        "owise": any(a == "owise" for a in attrs),
                        "macro": any(a in {"macro", "macro-rec"} for a in attrs),
                        "no_evaluators": any(a == "no-evaluators" for a in attrs),
                        "concrete": any(a == "concrete" for a in attrs),
                    },
                    "normalized_sha256": digest,
                    "text": text,
                }
            )

    by_kind = Counter(str(document["kind"]) for document in documents)
    by_file_kind: dict[str, Counter[str]] = {}
    for document in documents:
        by_file_kind.setdefault(str(document["path"]), Counter())[
            str(document["kind"])
        ] += 1
    attributes_counter = Counter(
        attribute
        for document in documents
        for attribute in document["attributes"]  # type: ignore[union-attr]
    )
    output = {
        "schema_version": 1,
        "source_files": [str(path) for path in ROOTS],
        "sentence_count": len(documents),
        "counts_by_kind": dict(sorted(by_kind.items())),
        "counts_by_file_and_kind": {
            path: dict(sorted(counts.items()))
            for path, counts in sorted(by_file_kind.items())
        },
        "attribute_counts": dict(sorted(attributes_counter.items())),
        "sentences": documents,
    }
    rendered = json.dumps(output, indent=2, sort_keys=True)
    output_path = Path("/audit-output/evidence/k-source-inventory.json")
    output_path.write_text(rendered + "\n", encoding="utf-8")
    print(f"files={len(ROOTS)} sentences={len(documents)}")
    print(f"counts_by_kind={dict(sorted(by_kind.items()))}")
    print(f"attribute_counts={dict(sorted(attributes_counter.items()))}")
    print(f"inventory_sha256={hashlib.sha256((rendered + chr(10)).encode()).hexdigest()}")


if __name__ == "__main__":
    main()
