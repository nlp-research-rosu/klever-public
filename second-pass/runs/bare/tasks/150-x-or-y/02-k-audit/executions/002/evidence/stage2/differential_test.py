#!/usr/bin/env python3
"""Independent differential/contract checks for HumanEval 150."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.x_or_y


def is_prime_math(n: int) -> bool:
    """Independent trial division, with the standard integer-prime domain."""
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


canonical = load_entry("trusted_canonical_150", Path("/tmp/audit-work/trusted/canonical.py"))
generated = load_entry("generated_solution_150", Path("/tmp/audit-work/candidate-src/solution.py"))

# Includes the prompt examples, both sides of n<2, loop-zero-iteration cases,
# the first composite branch, prime/composite squares, repeated factors, and
# representative larger values.  There is no collection-like "empty" input;
# n=0 is the numeric analogue and is included explicitly.
explicit = [
    (-7, 101, -303),
    (-1, 101, -303),
    (0, 101, -303),
    (1, 101, -303),
    (2, 101, -303),
    (3, 101, -303),
    (4, 101, -303),
    (5, 101, -303),
    (7, 34, 12),
    (8, 101, -303),
    (9, 101, -303),
    (15, 8, 5),
    (25, -8, 5),
    (29, -8, 5),
    (49, 0, 17),
    (97, 11, 22),
    (121, 11, 22),
    (9973, -999, 888),
    (10000, -999, 888),
]

print("EXPLICIT_CASES_BEGIN")
for n, x, y in explicit:
    expected = x if is_prime_math(n) else y
    got_generated = generated(n, x, y)
    got_canonical = canonical(n, x, y)
    print(
        f"n={n},x={x},y={y},math={expected},"
        f"generated={got_generated},canonical={got_canonical}"
    )
print("EXPLICIT_CASES_END")

assert generated(7, 34, 12) == 34
assert generated(15, 8, 5) == 5

rng = random.Random(150)
cases = [(n, 7 * n - 13, 101 - 3 * n) for n in range(-1000, 2001)]
cases.extend(
    (rng.randint(-100_000, 100_000), rng.randint(-10**9, 10**9), rng.randint(-10**9, 10**9))
    for _ in range(2000)
)

generated_contract_mismatches = []
canonical_contract_mismatches = []
generated_canonical_mismatches = []
positive_generated_canonical_mismatches = []
for n, x, y in cases:
    expected = x if is_prime_math(n) else y
    got_generated = generated(n, x, y)
    got_canonical = canonical(n, x, y)
    if got_generated != expected:
        generated_contract_mismatches.append((n, x, y, expected, got_generated))
    if got_canonical != expected:
        canonical_contract_mismatches.append((n, x, y, expected, got_canonical))
    if got_generated != got_canonical:
        generated_canonical_mismatches.append((n, x, y, got_generated, got_canonical))
        if n >= 1:
            positive_generated_canonical_mismatches.append(
                (n, x, y, got_generated, got_canonical)
            )

print(f"generated_case_count={len(cases)}")
print(f"generated_contract_mismatch_count={len(generated_contract_mismatches)}")
print(f"canonical_contract_mismatch_count={len(canonical_contract_mismatches)}")
print(f"generated_canonical_mismatch_count={len(generated_canonical_mismatches)}")
print(
    "positive_generated_canonical_mismatch_count="
    f"{len(positive_generated_canonical_mismatches)}"
)
print(
    "generated_canonical_mismatch_samples="
    f"{generated_canonical_mismatches[:12]}"
)

# The generated program satisfies the literal prime/non-prime contract on all
# tested integers and agrees with the trusted canonical on n >= 1.  The script
# deliberately reports (rather than hides) the canonical's n <= 0 behavior.
assert not generated_contract_mismatches
assert not positive_generated_canonical_mismatches
