#!/usr/bin/env python3
"""Summarize the generated K inventory without changing it."""

from __future__ import annotations

import collections
import csv
from pathlib import Path


path = Path("/audit-output/evidence/rule_inventory.tsv")
kind_counts: collections.Counter[str] = collections.Counter()
flag_counts: collections.Counter[str] = collections.Counter()
decision_counts: collections.Counter[str] = collections.Counter()

with path.open(encoding="utf-8", newline="") as stream:
    for row in csv.DictReader(stream, delimiter="\t"):
        kind_counts[row["kind"]] += 1
        decision_counts[row["decision"]] += 1
        for flag in row["flags"].split(","):
            if flag != "-":
                flag_counts[flag] += 1

print("ENTRIES", sum(kind_counts.values()))
for key, value in sorted(kind_counts.items()):
    print("KIND", key, value)
for key, value in sorted(flag_counts.items()):
    print("FLAG", key, value)
for key, value in sorted(decision_counts.items()):
    print("DECISION", key, value)
