#!/usr/bin/env python3
"""Independent differential test of the trusted canonical and submitted entry points."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_palindrome


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
submitted = load_entry(
    "submitted_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)

documented_examples = [3, 12]
empty_range_case = [0]  # Outside the stated domain; range(1, 0 + 1) is empty.
branch_boundaries = [
    1,
    2,
    8,
    9,
    10,
    11,
    12,
    98,
    99,
    100,
    101,
    109,
    110,
    111,
    199,
    200,
    201,
    899,
    900,
    901,
    998,
    999,
    1000,
]

generator = random.Random(107)
representative_generated = sorted(generator.sample(range(1, 1001), 80))
intended_domain = range(1, 1001)

print(
    "INPUTS:",
    json.dumps(
        {
            "documented_examples": documented_examples,
            "empty_range_case_outside_contract": empty_range_case,
            "branch_boundaries": branch_boundaries,
            "representative_generated_seed": 107,
            "representative_generated": representative_generated,
            "exhaustive_intended_domain": {"start": 1, "stop_inclusive": 1000},
        },
        sort_keys=True,
    ),
)

for name, values in (
    ("documented_examples", documented_examples),
    ("empty_range_case_outside_contract", empty_range_case),
    ("branch_boundaries", branch_boundaries),
    ("representative_generated", representative_generated),
):
    rows = [
        {
            "n": n,
            "canonical": canonical(n),
            "submitted": submitted(n),
            "match": canonical(n) == submitted(n),
        }
        for n in values
    ]
    print(f"RESULTS {name}:", json.dumps(rows, sort_keys=True))

intended_mismatches = [
    (n, canonical(n), submitted(n))
    for n in intended_domain
    if canonical(n) != submitted(n)
]
print(
    "EXHAUSTIVE_RESULT:",
    json.dumps(
        {
            "tested": 1000,
            "mismatch_count": len(intended_mismatches),
            "mismatches": intended_mismatches,
        },
        sort_keys=True,
    ),
)

sys.exit(1 if intended_mismatches else 0)
