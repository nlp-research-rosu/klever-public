#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval 90."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_entry(
    "audited_candidate", Path("/tmp/audit-work/candidate/solution.py")
)

# The labels identify examples, empty/singleton/duplicate boundaries, and every
# control-flow branch in the candidate implementation.
named_cases = [
    ("documented_ascending", [1, 2, 3, 4, 5]),
    ("documented_permuted", [5, 1, 4, 3, 2]),
    ("documented_empty", []),
    ("documented_no_second_distinct", [1, 1]),
    ("singleton", [7]),
    ("first_lower_than_initial_min", [2, 1]),
    ("first_greater_than_initial_min", [1, 2]),
    ("equal_to_minimum", [1, 1, 2]),
    ("new_min_after_second_known", [3, 5, 2]),
    ("between_min_and_second", [1, 5, 3]),
    ("equal_to_second", [1, 3, 3]),
    ("greater_than_second", [1, 3, 5]),
    ("zero_and_negative", [0, -1, 0]),
    ("negative_duplicates", [-1, -3, -2, -3]),
    ("large_magnitudes", [10**100, -(10**100), 0, 10**100]),
]


def check(values: list[int], label: str) -> None:
    expected = canonical(list(values))
    actual = candidate(list(values))
    if actual != expected:
        raise AssertionError(
            f"{label}: input={values!r}, canonical={expected!r}, candidate={actual!r}"
        )


for case_label, case_values in named_cases:
    check(case_values, case_label)
    print(
        f"NAMED {case_label}: input={case_values!r} "
        f"result={candidate(list(case_values))!r}"
    )

alphabet = (-2, -1, 0, 1, 2)
exhaustive_count = 0
for length in range(7):
    for values_tuple in itertools.product(alphabet, repeat=length):
        check(list(values_tuple), f"exhaustive_length_{length}")
        exhaustive_count += 1

rng = random.Random(0x90A11D17)
random_count = 5000
for random_index in range(random_count):
    length = rng.randint(0, 100)
    values = [
        rng.choice(
            (
                rng.randint(-(10**12), 10**12),
                -(10**100),
                -1,
                0,
                1,
                10**100,
            )
        )
        for _ in range(length)
    ]
    check(values, f"random_{random_index}")

print(
    "SUMMARY "
    f"named={len(named_cases)} exhaustive={exhaustive_count} "
    f"random={random_count} mismatches=0"
)
