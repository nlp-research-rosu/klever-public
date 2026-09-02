#!/usr/bin/env python3
"""Enumerate all K declarations and rules in the mounted fixed and proof theory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)
START = re.compile(
    r"^\s*(configuration|context|syntax|rule|claim|module|endmodule|imports)\b"
)
ATTRS = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "concrete",
    "priority",
    "simplification",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)


counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
attribute_lines: list[tuple[Path, int, list[str], str]] = []
print("K RULE/DECLARATION INVENTORY")
for path in FILES:
    lines = path.read_text().splitlines()
    relative = path.relative_to(ROOT)
    print(f"\nFILE {relative} lines={len(lines)} sha256_input=see provenance.log")
    for number, line in enumerate(lines, 1):
        line_attrs = [attr for attr in ATTRS if attr in line]
        if line_attrs:
            attribute_lines.append((relative, number, line_attrs, line.strip()))
            for attr in line_attrs:
                attribute_counts[attr] += 1
        match = START.match(line)
        if not match:
            continue
        kind = match.group(1)
        counts[kind] += 1
        present = line_attrs
        attr_text = ",".join(present) if present else "-"
        print(
            f"{relative}:{number}: {kind.upper()} attrs={attr_text} "
            f"{line.strip()}"
        )

print("\nTOTALS")
for kind, count in sorted(counts.items()):
    print(kind, count)
print("ATTRIBUTE_OCCURRENCES_ON_ALL_LINES")
for attr, count in sorted(attribute_counts.items()):
    print(attr, count)
print("\nALL ATTRIBUTE-BEARING LINES")
for relative, number, attrs, text in attribute_lines:
    print(f"{relative}:{number}: attrs={','.join(attrs)} {text}")
