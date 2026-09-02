#!/usr/bin/env python3
"""Summarize the exhaustive rule-inventory.tsv ledger."""

from __future__ import annotations

import collections
import csv
from pathlib import Path


rows = list(
    csv.DictReader(
        Path("/audit-output/evidence/rule-inventory.tsv").open(),
        delimiter="\t",
    )
)
print(f"items={len(rows)}")
for field in ("kind", "rule_class", "source_class", "audit_decision", "path_relevance"):
    counts = collections.Counter(row[field] for row in rows)
    print(field + "=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)))

for attribute in (
    "function",
    "total",
    "functional",
    "symbol(",
    "no-evaluators",
    "priority(",
    "simplification",
    "concrete",
    "macro",
):
    count = sum(attribute in row["normalized_text"] for row in rows)
    print(f"contains_{attribute}={count}")

print("candidate_rule_decisions:")
for row in rows:
    if row["source_class"] == "candidate-proof-extension" and row["kind"] == "rule":
        print(
            f"{row['file']}:{row['line']} "
            f"{row['rule_class']} {row['audit_decision']}"
        )
