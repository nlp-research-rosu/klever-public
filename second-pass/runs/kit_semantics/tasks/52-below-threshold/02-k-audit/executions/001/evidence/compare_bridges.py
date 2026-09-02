#!/usr/bin/env python3
"""Mechanically compare each operational bridge to its bridge-free claim."""

from __future__ import annotations

import csv
import re
from pathlib import Path


with Path("/audit-output/evidence/rule-inventory.tsv").open(newline="") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))

bridge_rows = [
    row
    for row in rows
    if row["file"] == "/candidate/verification.k" and row["kind"] == "rule"
]
claim_rows = [
    row
    for row in rows
    if row["file"] == "/candidate/loop-spec.k" and row["kind"] == "claim"
]


def normalize_bridge(text: str) -> str:
    text = re.sub(r"^rule\s+", "", text)
    text = re.sub(r"\s+\[priority\(40\)\]$", "", text)
    return text


def normalize_claim(text: str) -> str:
    return re.sub(r"^claim\s+\[[^\]]+\]:\s+", "", text)


if len(bridge_rows) != 4 or len(claim_rows) != 4:
    raise SystemExit(
        f"unexpected inventory size bridges={len(bridge_rows)} claims={len(claim_rows)}"
    )

all_equal = True
for index, (bridge, claim) in enumerate(zip(bridge_rows, claim_rows), 1):
    bridge_term = normalize_bridge(bridge["declaration"])
    claim_term = normalize_claim(claim["declaration"])
    equal = bridge_term == claim_term
    all_equal &= equal
    print(
        f"pair={index} bridge={bridge['file']}:{bridge['start_line']}-"
        f"{bridge['end_line']} claim={claim['file']}:{claim['start_line']}-"
        f"{claim['end_line']} exact_after_rule_metadata_normalization={equal}"
    )
    if not equal:
        print(f"bridge_normalized={bridge_term}")
        print(f"claim_normalized={claim_term}")

if not all_equal:
    raise SystemExit(1)

