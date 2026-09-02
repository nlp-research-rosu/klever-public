#!/usr/bin/env python3
"""Mechanical final checks for REVIEW.md and its local evidence links."""

from __future__ import annotations

import csv
import re
from pathlib import Path


review_path = Path("/audit-output/REVIEW.md")
review = review_path.read_text(encoding="utf-8")

expected_tail = "VERDICT: CONCERNS\nLEGITIMACY: LEGIT\n"
if not review.endswith(expected_tail):
    raise SystemExit("invalid verdict tail")

positions = []
for stage in range(1, 8):
    match = re.search(rf"^## {stage}\. ", review, flags=re.MULTILINE)
    if match is None:
        raise SystemExit(f"missing stage {stage}")
    positions.append(match.start())
if positions != sorted(positions):
    raise SystemExit("stages out of order")

links = re.findall(r"\]\((evidence/[^)]+)\)", review)
missing = [
    target
    for target in links
    if not (review_path.parent / target).is_file()
]
if missing:
    raise SystemExit(f"missing evidence links: {missing}")

inventory_path = Path("/audit-output/evidence/k_inventory.csv")
rows = list(csv.DictReader(inventory_path.open(encoding="utf-8")))
kind_counts: dict[str, int] = {}
for row in rows:
    kind_counts[row["kind"]] = kind_counts.get(row["kind"], 0) + 1

print(f"STAGES_IN_ORDER: {len(positions)}")
print(f"EVIDENCE_LINKS: {len(links)}")
print("MISSING_EVIDENCE_LINKS: 0")
print(f"INVENTORY_ROWS: {len(rows)}")
print(f"INVENTORY_RULES: {kind_counts.get('rule', 0)}")
print(f"INVENTORY_SYNTAX: {kind_counts.get('syntax', 0)}")
print("VERDICT_TAIL_VALID: yes")
