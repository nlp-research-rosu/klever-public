#!/usr/bin/env python3
"""Independent differential test for HumanEval/59.

The oracle is implemented independently from both the canonical scan and the
candidate's residual-division implementation.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


def independent_oracle(value: int) -> int:
    residual = value
    largest = 1
    divisor = 2
    while divisor * divisor <= residual:
        while residual % divisor == 0:
            largest = divisor
            residual //= divisor
        divisor += 1
    if residual > 1:
        largest = residual
    return largest


canonical = load_entry(
    "trusted_canonical",
    Path("/tmp/audit-work/59-largest-prime-factor/trusted/canonical.py"),
)
generated = load_entry(
    "candidate_solution",
    Path("/tmp/audit-work/59-largest-prime-factor/source/solution.py"),
)

# No "empty" scalar integer exists.  Four is the smallest contract-valid
# input.  These named cases exercise loop entry/non-entry after division,
# exact factor-square equality, the divisible and non-divisible branches,
# repeated factors, semiprimes, and the two documented examples.
named_cases = {
    "smallest-composite": 4,
    "first-nondivisible-step": 6,
    "repeated-factor": 8,
    "factor-square-boundary": 9,
    "mixed-small-factors": 12,
    "odd-semiprime": 15,
    "power-of-two": 2048,
    "documented-mixed": 13195,
    "square-of-prime": 169,
    "larger-semiprime": 1763,  # 41 * 43
}

tested: set[int] = set()


def check(value: int, label: str) -> None:
    expected = independent_oracle(value)
    canonical_result = canonical(value)
    generated_result = generated(value)
    assert canonical_result == expected, (
        label,
        value,
        canonical_result,
        expected,
    )
    assert generated_result == expected, (
        label,
        value,
        generated_result,
        expected,
    )
    tested.add(value)


for label, value in named_cases.items():
    check(value, label)
    print(
        f"NAMED {label} n={value} "
        f"result={generated(value)} canonical={canonical(value)}"
    )

# Exhaust every contract-valid composite through 4,999.
for value in range(4, 5000):
    if any(value % divisor == 0 for divisor in range(2, math.isqrt(value) + 1)):
        check(value, "exhaustive-small-composite")

# Seeded representative composite values beyond the exhaustive range.
rng = random.Random(590059)
for _ in range(256):
    left = rng.randint(2, 199)
    right = rng.randint(2, 199)
    check(left * right, "seeded-product")

# The formal candidate claim is broader than the source contract, so also
# compare prime inputs on a bounded sample.  These do not count toward the
# source-contract domain check.
for value in range(2, 200):
    if all(value % divisor for divisor in range(2, math.isqrt(value) + 1)):
        check(value, "extra-domain-prime")

print(f"TOTAL_DISTINCT_INPUTS {len(tested)}")
print("MISMATCHES 0")
