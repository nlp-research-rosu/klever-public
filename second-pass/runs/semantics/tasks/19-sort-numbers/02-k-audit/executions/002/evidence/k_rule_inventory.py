#!/usr/bin/env python3
"""Produce a deterministic inventory of K declarations and rules under audit."""

from __future__ import annotations

import collections
import pathlib
import re

root = pathlib.Path("/tmp/audit-work/review-19/candidate")
paths = sorted((root / "reference-semantics").rglob("*.k"))
paths.append(root / "verification.k")
paths.append(root / "spec.k")

start_re = re.compile(
    r'^\s*(requires(?=\s+"[^"]+\.k")|module|endmodule|imports|configuration|'
    r"syntax|context(?:\s+alias)?|rule|claim)\b"
)

kind_counts: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()
file_counts: dict[str, collections.Counter[str]] = {}
records: list[tuple[str, int, str, str, list[str]]] = []

for path in paths:
    relative = str(path.relative_to(root))
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_re.match(line) and not line.lstrip().startswith("//")
    ]
    starts.append(len(lines))
    counts: collections.Counter[str] = collections.Counter()
    for offset, start in enumerate(starts[:-1]):
        first = lines[start].strip()
        kind_match = start_re.match(lines[start])
        assert kind_match is not None
        kind = kind_match.group(1)
        end = starts[offset + 1]
        block_lines = [
            line.strip()
            for line in lines[start:end]
            if line.strip() and not line.lstrip().startswith("//")
        ]
        compact = " ".join(block_lines)
        attrs: list[str] = []
        for attribute in [
            "macro",
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "strict",
            "seqstrict",
        ]:
            if re.search(rf"\b{re.escape(attribute)}\b", compact):
                attrs.append(attribute)
                attribute_counts[attribute] += 1
        kind_counts[kind] += 1
        counts[kind] += 1
        records.append((relative, start + 1, kind, compact, attrs))
    file_counts[relative] = counts

print("AUDITED_FILES:", len(paths))
print("TOTAL_RECORDS:", len(records))
print("KIND_COUNTS:", dict(sorted(kind_counts.items())))
print("ATTRIBUTE_RECORD_COUNTS:", dict(sorted(attribute_counts.items())))
print("FILE_COUNTS:")
for relative, counts in file_counts.items():
    print(f"  {relative}: {dict(sorted(counts.items()))}")
print("RECORDS:")
for relative, line, kind, compact, attrs in records:
    attr_text = ",".join(attrs) if attrs else "-"
    print(
        f"{relative}:{line} | {kind} | attrs={attr_text} | "
        f"{compact}"
    )
