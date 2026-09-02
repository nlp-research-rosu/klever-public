#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of local K declarations."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
FILES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
STARTS = ("syntax ", "rule ", "context ", "configuration", "claim")
ATTR_PATTERNS = [
    "function",
    "total",
    "functional",
    "no-evaluators",
    "simplification",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "macro",
    "macro-rec",
    "symbol",
]


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if line.strip().startswith(STARTS)
    ]
    for number, index in enumerate(starts):
        hard_end = starts[number + 1] if number + 1 < len(starts) else len(lines)
        end = index + 1
        while end < hard_end:
            stripped = lines[end].strip()
            if not stripped or stripped.startswith("//") or stripped in {"endmodule"}:
                break
            end += 1
        text = " ".join(line.strip() for line in lines[index:end])
        text = re.sub(r"\s+", " ", text)
        yield index + 1, text


kind_counts = collections.Counter()
attribute_counts = collections.Counter()
file_counts = collections.Counter()
records = []

for path in FILES:
    assert path.is_file(), path
    relative = (
        path.relative_to(ROOT).as_posix()
        if path.is_relative_to(ROOT)
        else path.as_posix()
    )
    for line, text in blocks(path):
        kind = text.split()[0]
        kind_counts[kind] += 1
        file_counts[relative] += 1
        attrs = []
        for attr in ATTR_PATTERNS:
            if re.search(rf"(?<![A-Za-z-]){re.escape(attr)}(?![A-Za-z-])", text):
                attrs.append(attr)
                attribute_counts[attr] += 1
        priorities = re.findall(r"priority\([^)]*\)", text)
        attrs.extend(priorities)
        for priority in priorities:
            attribute_counts[priority] += 1
        records.append((relative, line, kind, ",".join(attrs) or "-", text))

print("# Exhaustive K declaration/rule inventory")
print()
print(f"Files: {len(FILES)}")
print(f"Records: {len(records)}")
print(f"Kind counts: {dict(sorted(kind_counts.items()))}")
print(f"Attribute counts: {dict(sorted(attribute_counts.items()))}")
print()
print("| File:line | Kind | Attributes | Declaration/rule |")
print("|---|---|---|---|")
for relative, line, kind, attrs, text in records:
    escaped = text.replace("|", "\\|")
    print(f"| `{relative}:{line}` | {kind} | {attrs} | `{escaped}` |")

print()
print("INVENTORY_COMPLETE=PASS")
