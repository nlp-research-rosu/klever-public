#!/usr/bin/env python3
"""Emit focused slices from the exhaustive K inventory for human review."""

from __future__ import annotations

import json
from pathlib import Path


inventory = Path("/audit-output/evidence/k-declaration-inventory.jsonl")
records = [
    json.loads(line)
    for line in inventory.read_text(encoding="utf-8").splitlines()
    if line
]

print("PROOF_LOCAL_DECLARATIONS")
for record in records:
    if record["source_class"] == "PROOF_LOCAL":
        print(
            f'{record["file"]}:{record["start_line"]}-{record["end_line"]} '
            f'kind={record["kind"]} tags={",".join(record["tags"]) or "-"} '
            f'decision={record["audit_decision"]}'
        )
        print("  " + " ".join(record["statement"].split()))

print("\nTARGET_CLAIMS")
for record in records:
    if record["source_class"] == "TARGET_CLAIM":
        print(
            f'{record["file"]}:{record["start_line"]}-{record["end_line"]} '
            f'{record["audit_decision"]}'
        )
        print("  " + " ".join(record["statement"].split()))

print("\nUSED_SUPPLIED_BASELINE_DECLARATIONS")
for record in records:
    if (
        record["source_class"] == "SUPPLIED_BASELINE"
        and record["relevance"].startswith("USED:")
    ):
        print(
            f'{record["file"]}:{record["start_line"]}-{record["end_line"]} '
            f'kind={record["kind"]} tags={",".join(record["tags"]) or "-"} '
            f'{record["relevance"]}'
        )

print("\nOPAQUE_OR_NO_EVALUATOR_DECLARATIONS")
opaque = [
    record
    for record in records
    if "no-evaluators" in record["tags"]
    or "opaque" in " ".join(record["attributes"]).lower()
]
for record in opaque:
    print(
        f'{record["file"]}:{record["start_line"]}-{record["end_line"]} '
        f'tags={",".join(record["tags"])} relevance={record["relevance"]}'
    )
    print("  " + " ".join(record["statement"].split()))
print(f"opaque-or-no-evaluator-count={len(opaque)}")

print("\nSPECIAL_DECLARATION_COUNTS")
for tag in (
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "symbol",
    "no-evaluators",
):
    count = sum(tag in record["tags"] for record in records)
    proof_count = sum(
        tag in record["tags"] and record["source_class"] == "PROOF_LOCAL"
        for record in records
    )
    print(f"{tag}: all={count} proof-local={proof_count}")
