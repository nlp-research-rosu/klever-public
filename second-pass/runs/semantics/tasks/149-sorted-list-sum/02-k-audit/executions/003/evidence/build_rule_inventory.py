#!/usr/bin/env python3
"""Emit an exhaustive source-level K sentence inventory with line ranges."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/149-sorted-list-sum")
files = [ROOT / "reference-semantics/semantics.k"]
files += sorted((ROOT / "reference-semantics/semantics").glob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

starter = re.compile(r"^  (configuration|syntax|context|rule|claim)\b")
attribute_names = (
    "function",
    "total",
    "functional",
    "no-evaluators",
    "symbol",
    "macro",
    "strict",
    "seqstrict",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "anywhere",
)

global_counts: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()
sentence_number = 0

print("# Exhaustive K source inventory")
print()
print("Roots: trusted supplied semantics copy, candidate verification.k, candidate spec.k.")
print()

for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = starter.match(line)
        if match:
            starts.append((index, match.group(1)))
    records = []
    for position, (start, category) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        for index in range(start + 1, next_start):
            if lines[index].startswith("endmodule"):
                end = index
                break
        text_lines = lines[start:end]
        while text_lines and (not text_lines[-1].strip() or text_lines[-1].lstrip().startswith("//")):
            text_lines.pop()
            end -= 1
        normalized = " ".join(
            line.strip()
            for line in text_lines
            if line.strip() and not line.lstrip().startswith("//")
        )
        attrs = [name for name in attribute_names if re.search(rf"\b{re.escape(name)}\b", normalized)]
        records.append((start + 1, end, category, normalized, attrs))
        global_counts[category] += 1
        attribute_counts.update(attrs)

    relative = path.relative_to(ROOT)
    print(f"## {relative}")
    print()
    print(f"Sentence count: {len(records)}")
    print()
    for start, end, category, normalized, attrs in records:
        sentence_number += 1
        attr_text = ",".join(attrs) if attrs else "-"
        print(
            f"{sentence_number:04d}\t{category.upper()}\t"
            f"{relative}:{start}-{end}\tATTRS={attr_text}\t{normalized}"
        )
    print()

print("# Totals")
print()
print(f"sentences={sentence_number}")
for category, count in sorted(global_counts.items()):
    print(f"{category}={count}")
for attribute, count in sorted(attribute_counts.items()):
    print(f"attribute_{attribute}={count}")
