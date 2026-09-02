#!/usr/bin/env python3
"""Ground witnesses for every candidate claim and each entry precondition."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


canonical = load_entry(
    Path("/tmp/audit-work/reference/canonical.py"), "canonical_claim_witness"
)
generated = load_entry(
    Path("/tmp/audit-work/src/solution.py"), "generated_claim_witness"
)

entry_cases = [
    {
        "claim": "first-when-no-greater",
        "lst1": ["a"],
        "lst2": ["bb"],
        "relation": "<=",
        "claimed_side": "lst1",
    },
    {
        "claim": "second-when-smaller",
        "lst1": ["bb"],
        "lst2": ["a"],
        "relation": ">",
        "claimed_side": "lst2",
    },
    {
        "claim": "first-on-tie",
        "lst1": ["a"],
        "lst2": ["b"],
        "relation": "==",
        "claimed_side": "lst1",
    },
]

records = [
    {
        "claim": "empty-total",
        "formal_state": "totalChars(.StrVals)",
        "expected": 0,
        "satisfiable": True,
    },
    {
        "claim": "cons-total",
        "formal_state": 'totalChars(pyStr(\"a\") :: .StrVals)',
        "expected": "lengthString(\"a\") + totalChars(.StrVals) = 1",
        "satisfiable": True,
    },
]

for case in entry_cases:
    left = case["lst1"]
    right = case["lst2"]
    left_total = sum(map(len, left))
    right_total = sum(map(len, right))
    actual_relation = (
        "<=" if left_total < right_total else ">" if left_total > right_total else "=="
    )
    canonical_result = canonical(left, right)
    generated_result = generated(left, right)
    expected = left if case["claimed_side"] == "lst1" else right
    records.append(
        {
            **case,
            "totals": [left_total, right_total],
            "actual_relation": actual_relation,
            "canonical_result": canonical_result,
            "generated_result": generated_result,
            "expected_result": expected,
            "both_match_claim": canonical_result == generated_result == expected,
            "satisfiable": True,
        }
    )

print(json.dumps(records, indent=2, ensure_ascii=True, sort_keys=True))
if not all(record["satisfiable"] for record in records):
    raise SystemExit(1)
if not all(record.get("both_match_claim", True) for record in records):
    raise SystemExit(1)
