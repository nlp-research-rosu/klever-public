#!/usr/bin/env python3
"""Exhaustive textual declaration inventory for the audited K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/rebuild")
sources = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

start_re = re.compile(r"^\s*(configuration|syntax|context|alias|rule|claim)\b")
boundary_re = re.compile(
    r"^\s*(configuration|syntax|context|alias|rule|claim|"
    r"module|endmodule|imports)\b"
)
attribute_names = [
    "function",
    "total",
    "functional",
    "no-evaluators",
    "symbol",
    "macro",
    "priority",
    "simplification",
    "owise",
    "strict",
    "seqstrict",
]

counts: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()
records: list[tuple[Path, int, str, str]] = []

for path in sources:
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = start_re.match(lines[index])
        if match is None:
            index += 1
            continue
        start = index
        kind = match.group(1)
        index += 1
        while index < len(lines) and not boundary_re.match(lines[index]):
            index += 1
        text = "\n".join(lines[start:index]).rstrip()
        records.append((path, start + 1, kind, text))
        counts[kind] += 1
        for attribute in attribute_names:
            if re.search(rf"\b{re.escape(attribute)}\b", text):
                attribute_counts[attribute] += 1

print(f"SOURCE_COUNT {len(sources)}")
print(f"DECLARATION_COUNT {len(records)}")
print("KIND_COUNTS " + " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
print(
    "ATTRIBUTE_COUNTS "
    + " ".join(f"{k}={v}" for k, v in sorted(attribute_counts.items()))
)

for number, (path, line, kind, text) in enumerate(records, 1):
    rel = path.relative_to(ROOT)
    origin = "CANDIDATE_LOCAL" if rel in {
        Path("verification.k"),
        Path("spec.k"),
    } else "SUPPLIED_FIXED"
    attributes = [
        attribute
        for attribute in attribute_names
        if re.search(rf"\b{re.escape(attribute)}\b", text)
    ]
    print(
        f"\nDECL {number:04d} origin={origin} kind={kind} "
        f"location={rel}:{line} attributes={','.join(attributes) or '-'}"
    )
    print(text)
