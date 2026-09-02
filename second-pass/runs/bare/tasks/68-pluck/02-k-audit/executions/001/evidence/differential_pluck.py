#!/usr/bin/env python3
"""Independent differential audit for HumanEval 68-pluck."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


canonical = load_function(Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical")
generated = load_function(
    Path("/tmp/audit-work/candidate-source/solution.py"), "candidate_solution"
)

fixed_cases = [
    # Four documented examples.
    [4, 2, 3],
    [1, 2, 3],
    [],
    [5, 0, 3, 0, 4, 2],
    # Empty/nonempty, no-even/even, zero, tie, and minimum-position boundaries.
    [1],
    [2],
    [0],
    [1, 3, 5],
    [2, 2],
    [4, 2],
    [2, 4],
    [3, 4, 2],
    [3, 2, 4],
    [0, 2, 0],
    [10**100 + 1, 10**100, 2, 4],
]

mismatches: list[dict[str, object]] = []
checked = 0


def check(case: list[int], group: str, emit: bool = False) -> None:
    global checked
    original = list(case)
    try:
        expected = canonical(case)
        expected_error = None
    except Exception as err:  # compare exceptional behavior as well
        expected = None
        expected_error = (type(err).__name__, str(err))
    try:
        actual = generated(case)
        actual_error = None
    except Exception as err:
        actual = None
        actual_error = (type(err).__name__, str(err))
    checked += 1
    if (
        expected != actual
        or expected_error != actual_error
        or case != original
    ):
        mismatches.append(
            {
                "group": group,
                "input": original,
                "canonical": expected,
                "candidate": actual,
                "canonical_error": expected_error,
                "candidate_error": actual_error,
                "post_input": case,
            }
        )
    if emit:
        print(
            json.dumps(
                {
                    "group": group,
                    "input": original,
                    "canonical": expected,
                    "candidate": actual,
                    "canonical_error": expected_error,
                    "candidate_error": actual_error,
                },
                sort_keys=True,
            )
        )


for fixed_case in fixed_cases:
    check(fixed_case, "fixed", emit=True)

# Exhaust all lists of length 0..6 over 0..5: exact scope is preserved here.
exhaustive_count = 0
for length in range(7):
    for values in itertools.product(range(6), repeat=length):
        check(list(values), "exhaustive")
        exhaustive_count += 1

# Deterministic representative generation over the full nonnegative value range.
rng = random.Random(680068)
random_count = 1000
for _ in range(random_count):
    length = rng.randrange(0, 101)
    case = [rng.randrange(0, 10**12 + 1) for _ in range(length)]
    check(case, "random")

# Documented maximum-length boundary and adversarial placement/tie cases.
large_cases = [
    [2 * i + 1 for i in range(10000)],
    [2 * i + 1 for i in range(9999)] + [0],
    [10000] + [2 * i + 1 for i in range(9998)] + [0],
    [8] * 10000,
]
for large_case in large_cases:
    check(large_case, "length-10000")

print(
    json.dumps(
        {
            "fixed_count": len(fixed_cases),
            "exhaustive_domain": {
                "lengths": [0, 1, 2, 3, 4, 5, 6],
                "values": [0, 1, 2, 3, 4, 5],
                "count": exhaustive_count,
            },
            "random_seed": 680068,
            "random_count": random_count,
            "random_lengths": "0..100",
            "random_values": "0..10^12",
            "length_10000_count": len(large_cases),
            "total_checked": checked,
            "mismatch_count": len(mismatches),
            "first_mismatches": mismatches[:10],
        },
        sort_keys=True,
    )
)

raise SystemExit(1 if mismatches else 0)
