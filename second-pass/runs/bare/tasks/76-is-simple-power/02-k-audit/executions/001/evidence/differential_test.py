#!/usr/bin/env python3
"""Independent differential checks for HumanEval 76.

The main exhaustive/generated domain is integer x with positive integer n.
That is the terminating domain supported uniformly by the trusted canonical
implementation. Separate probes retain prompt-relevant negative-base witnesses.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import Callable


def load_function(path: Path, module_name: str) -> Callable[[int, int], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


def independent_math_oracle(x: int, n: int) -> bool:
    """Check x=n**e for a nonnegative integer e, for positive integer n."""
    if x == 1:
        return True
    if x < 1 or n < 2:
        return False
    reduced = x
    while reduced % n == 0:
        reduced //= n
    return reduced == 1


canonical = load_function(
    Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical"
)
generated = load_function(
    Path("/tmp/audit-work/source/solution.py"), "generated_solution"
)

documented = [(1, 4), (2, 2), (8, 2), (3, 2), (3, 1), (5, 3)]
branch_boundaries = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 2),
    (4, 2),
    (5, 2),
    (8, 2),
    (9, 3),
    (10, 3),
]
exhaustive_small = [(x, n) for x in range(-20, 501) for n in range(1, 13)]
rng = random.Random(76076)
generated_inputs = [(rng.randint(-100, 100_000), rng.randint(1, 20)) for _ in range(2000)]

ordered_cases = []
seen = set()
for case in documented + branch_boundaries + exhaustive_small + generated_inputs:
    if case not in seen:
        seen.add(case)
        ordered_cases.append(case)

mismatches = []
for x, n in ordered_cases:
    expected = canonical(x, n)
    actual = generated(x, n)
    math_value = independent_math_oracle(x, n)
    if not (expected == actual == math_value):
        mismatches.append((x, n, expected, actual, math_value))

print(f"documented_cases={documented}")
print(f"branch_boundary_cases={branch_boundaries}")
print("exhaustive_small_domain=x:-20..500,n:1..12")
print("generated_domain=2000 seeded pairs,x:-100..100000,n:1..20,seed:76076")
print(f"unique_positive_base_cases={len(ordered_cases)}")
print(f"positive_base_mismatch_count={len(mismatches)}")
print(f"positive_base_mismatches={mismatches[:20]}")

# The literal prompt does not state n > 0. These terminating canonical cases
# show that treating all bases below 2 as false is not canonical-equivalent and
# is not equivalent to the ordinary n**e reading.
negative_base_witnesses = [(4, -2), (9, -3), (16, -2), (81, -3)]
negative_rows = []
for x, n in negative_base_witnesses:
    # Every selected x is n raised to a nonnegative even exponent.
    ordinary_expected = any(n**exponent == x for exponent in range(0, 12))
    negative_rows.append(
        (x, n, canonical(x, n), generated(x, n), ordinary_expected)
    )
print(f"negative_base_witnesses={negative_rows}")
print(
    "negative_base_columns=(x,n,canonical,generated,"
    "ordinary_nonnegative_exponent_expected)"
)

if mismatches:
    raise SystemExit(1)
