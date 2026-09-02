#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/72."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(module_name: str, path: Path) -> Callable[[list[Any], Any], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry("generated_candidate", Path("/candidate/solution.py"))


documented_and_boundary_cases: list[tuple[list[Any], Any, bool]] = [
    ([1, 2], 5, False),       # documented, light but unbalanced
    ([3, 2, 3], 1, False),    # documented, balanced but overweight
    ([3, 2, 3], 9, True),     # documented, exactly at capacity
    ([3], 5, True),           # documented singleton
    ([], -1, False),          # empty sum just above capacity
    ([], 0, True),            # empty and exact boundary
    ([0], -1, False),         # singleton overweight by one
    ([0], 0, True),           # singleton exact boundary
    ([1, 1], 1, False),       # balanced length two, overweight
    ([1, 1], 2, True),        # balanced length two, exact boundary
    ([1, 2], 3, False),       # unbalanced, exact sum boundary
    ([-4, 1, -4], -7, True), # negative exact sum boundary
    ([-4, 1, -4], -8, False),
    ([10**100, 0, 10**100], 2 * 10**100, True),
    ([False, True, False], 1, True),
    ([1.5, -0.5, 1.5], 2.5, True),
    ([1, 0.5, 1], 2.4, False),
    ([1, True], 2, True),     # CPython's numeric equality boundary
]


def check(q: list[Any], w: Any, expected: bool | None = None) -> None:
    global checked
    canonical_result = canonical(q, w)
    candidate_result = candidate(q, w)
    assert type(canonical_result) is bool
    assert type(candidate_result) is bool
    assert canonical_result == candidate_result, (q, w, canonical_result, candidate_result)
    if expected is not None:
        assert canonical_result == expected, (q, w, canonical_result, expected)
    checked += 1


checked = 0
for case_q, case_w, case_expected in documented_and_boundary_cases:
    check(case_q, case_w, case_expected)
fixed_count = checked

# Exhaustively cross every integer-list branch boundary for modest sizes.
for length in range(6):
    for values in itertools.product(range(-3, 4), repeat=length):
        q = list(values)
        for w in range(-9, 10):
            check(q, w)
integer_exhaustive_count = checked - fixed_count

# Representative Python numeric combinations, including Bool/Int/Float mixing.
numeric_values = [False, True, -2, 0, 3, -0.5, 1.5]
numeric_weights = [-4, -0.5, 0, 1, 3.5, 8]
before_numeric = checked
for length in range(5):
    for values in itertools.product(numeric_values, repeat=length):
        for w in numeric_weights:
            check(list(values), w)
numeric_exhaustive_count = checked - before_numeric

# Deterministic longer generated cases exercise unbounded-shape representatives.
rng = random.Random(720072)
before_random = checked
for _ in range(10_000):
    length = rng.randrange(0, 41)
    q = [rng.randrange(-10_000, 10_001) for _ in range(length)]
    if rng.random() < 0.5:
        q = q[: (length + 1) // 2] + q[: length // 2][::-1]
    w = rng.randrange(-100_000, 100_001)
    check(q, w)
random_count = checked - before_random

print(f"fixed_documented_boundary_cases={fixed_count}")
print(f"exhaustive_integer_cases={integer_exhaustive_count}")
print(f"exhaustive_mixed_numeric_cases={numeric_exhaustive_count}")
print(f"deterministic_random_long_cases={random_count}")
print(f"total_cases={checked}")
print("mismatches=0")
