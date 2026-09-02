#!/usr/bin/env python3
"""Emit an exhaustive, source-located inventory of local K declarations."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/96-count-up-to/source")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

START = re.compile(
    r"^(?P<indent>\s*)(?P<kind>configuration|syntax|context|rule|claim)\b"
)
BOUNDARY = re.compile(
    r"^(?P<indent>\s*)(?P<kind>"
    r"configuration|syntax|context|rule|claim|module|endmodule|imports"
    r")\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)\b")


def blocks(path: Path):
    lines = path.read_text().splitlines()
    module = "(outside module)"
    index = 0
    while index < len(lines):
        module_match = MODULE.match(lines[index])
        if module_match:
            module = module_match.group(1)
        start = START.match(lines[index])
        if not start:
            index += 1
            continue
        indent = len(start.group("indent"))
        kind = start.group("kind")
        end = index + 1
        while end < len(lines):
            boundary = BOUNDARY.match(lines[end])
            if boundary and len(boundary.group("indent")) <= indent:
                break
            end += 1
        text_lines = lines[index:end]
        while text_lines and (
            not text_lines[-1].strip()
            or text_lines[-1].lstrip().startswith("//")
        ):
            text_lines.pop()
        yield {
            "path": path.relative_to(ROOT).as_posix(),
            "module": module,
            "line": index + 1,
            "kind": kind,
            "text": "\n".join(text_lines),
        }
        index = end


items = [item for path in FILES for item in blocks(path)]
kind_counts = Counter(item["kind"] for item in items)
file_counts = Counter(item["path"] for item in items)
attribute_counts = Counter()
for item in items:
    attribute_text = " ".join(re.findall(r"\[([^\]]*)\]", item["text"], re.S))
    for attribute in (
        "function",
        "total",
        "functional",
        "symbol",
        "no-evaluators",
        "simplification",
        "concrete",
        "priority",
        "owise",
        "strict",
        "seqstrict",
        "macro",
    ):
        if re.search(rf"\b{re.escape(attribute)}\b", attribute_text):
            attribute_counts[attribute] += 1

print("# Exhaustive K declaration and rule inventory")
print()
print(f"Source root: `{ROOT}`")
print()
print(f"Files: {len(FILES)}")
print(f"Inventoried blocks: {len(items)}")
print(f"Block counts: {dict(sorted(kind_counts.items()))}")
print(f"Attribute-bearing block counts: {dict(sorted(attribute_counts.items()))}")
print("Per-file block counts:")
for path, count in sorted(file_counts.items()):
    print(f"- `{path}`: {count}")
print()

for ordinal, item in enumerate(items, 1):
    text = item["text"]
    attribute_text = " ".join(re.findall(r"\[([^\]]*)\]", text, re.S))
    attrs = [
        attr
        for attr in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "simplification",
            "concrete",
            "priority",
            "owise",
            "strict",
            "seqstrict",
            "macro",
        )
        if re.search(rf"\b{re.escape(attr)}\b", attribute_text)
    ]
    print(
        f"## {ordinal}. {item['kind']} — `{item['path']}:{item['line']}` "
        f"(module `{item['module']}`)"
    )
    print()
    print(f"Attributes/classifiers: {', '.join(attrs) if attrs else 'none'}")
    print()
    print("```k")
    print(text)
    print("```")
    print()
