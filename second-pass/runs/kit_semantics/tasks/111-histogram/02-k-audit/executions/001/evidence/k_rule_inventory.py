#!/usr/bin/env python3
"""Lexical inventory of every local K sentence and soundness-relevant attribute."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/111-histogram-audit")
paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths += [ROOT / "verification.k", ROOT / "spec.k"]

sentence_re = re.compile(
    r"^\s*(syntax|configuration|rule|context|context\s+alias|claim|macro|alias)\b"
)
attribute_terms = (
    "function",
    "functional",
    "total",
    "no-evaluators",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "strict",
    "seqstrict",
)
counts: collections.Counter[str] = collections.Counter()
file_counts: dict[str, collections.Counter[str]] = {}
records: list[tuple[str, int, str, str]] = []
attribute_records: list[tuple[str, int, str]] = []

for path in paths:
    relative = str(path.relative_to(ROOT))
    file_counts[relative] = collections.Counter()
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, 1):
        match = sentence_re.match(line)
        if match:
            kind = " ".join(match.group(1).split())
            counts[kind] += 1
            file_counts[relative][kind] += 1
            records.append((relative, line_number, kind, line.strip()))
        if "[" in line and any(term in line for term in attribute_terms):
            attribute_records.append((relative, line_number, line.strip()))

print(f"K source files inventoried: {len(paths)}")
for path in paths:
    print(f"  FILE {path.relative_to(ROOT)}")
print(f"sentence-start counts: {dict(sorted(counts.items()))}")
print("per-file sentence-start counts:")
for relative, relative_counts in file_counts.items():
    print(f"  {relative}: {dict(sorted(relative_counts.items()))}")
print(f"soundness-relevant attribute lines: {len(attribute_records)}")
print("SENTENCE INVENTORY")
for relative, line_number, kind, text in records:
    print(f"{relative}:{line_number}: {kind}: {text}")
print("ATTRIBUTE INVENTORY")
for relative, line_number, text in attribute_records:
    print(f"{relative}:{line_number}: {text}")
