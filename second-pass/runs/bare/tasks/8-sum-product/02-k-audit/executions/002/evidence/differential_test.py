#!/usr/bin/env python3
"""Independent differential test for HumanEval/8.

The input set is deterministic: named boundary cases followed by every list
of length 0 through 5 over (-3, -1, 0, 1, 2, 5).
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import sys


SCRATCH = Path("/tmp/audit-work/reconstruction-8-sum-product")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load_function("trusted_canonical", SCRATCH / "reference/canonical.py")
generated = load_function("candidate_generated", SCRATCH / "candidate/solution.py")

named_cases = [
    ("documented_empty", []),
    ("documented_four_positive", [1, 2, 3, 4]),
    ("singleton_zero", [0]),
    ("singleton_one", [1]),
    ("singleton_minus_one", [-1]),
    ("zero_in_middle", [-2, 0, 5]),
    ("two_negatives", [-7, -11]),
    ("mixed_sign", [-7, 3, 5]),
    ("large_magnitude", [10**40, -(10**30), 17]),
]

pool = (-3, -1, 0, 1, 2, 5)
exhaustive_cases = (
    (f"exhaustive_len_{length}", list(values))
    for length in range(0, 6)
    for values in itertools.product(pool, repeat=length)
)

mismatches = []
checked = 0
for label, values in itertools.chain(named_cases, exhaustive_cases):
    canonical_input = list(values)
    generated_input = list(values)
    try:
        expected = canonical(canonical_input)
        expected_exc = None
    except Exception as error:  # retained to compare exceptional behavior
        expected = None
        expected_exc = (type(error).__name__, str(error))
    try:
        actual = generated(generated_input)
        actual_exc = None
    except Exception as error:
        actual = None
        actual_exc = (type(error).__name__, str(error))
    checked += 1
    if (
        expected != actual
        or expected_exc != actual_exc
        or canonical_input != values
        or generated_input != values
    ):
        mismatches.append(
            {
                "label": label,
                "input": values,
                "canonical": expected,
                "candidate": actual,
                "canonical_exception": expected_exc,
                "candidate_exception": actual_exc,
                "canonical_input_after": canonical_input,
                "candidate_input_after": generated_input,
            }
        )

summary = {
    "entry_point": "sum_product",
    "named_cases": len(named_cases),
    "exhaustive_pool": list(pool),
    "exhaustive_lengths": [0, 1, 2, 3, 4, 5],
    "total_cases": checked,
    "mismatch_count": len(mismatches),
    "first_mismatches": mismatches[:10],
}
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(1 if mismatches else 0)
