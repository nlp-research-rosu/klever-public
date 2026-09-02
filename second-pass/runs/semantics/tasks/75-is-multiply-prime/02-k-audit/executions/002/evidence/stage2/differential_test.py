#!/usr/bin/env python3
"""Differential test: trusted HumanEval canonical vs submitted Python program."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_three_prime_factors(value: int) -> bool:
    """Mathematical oracle, independent of either implementation."""
    if value < 2:
        return False
    count = 0
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            count += 1
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        count += 1
    return count == 3


canonical_module = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated_module = load_module(
    "submitted_solution",
    Path("/tmp/audit-work/75-is-multiply-prime/solution.py"),
)
canonical = canonical_module.is_multiply_prime
generated = generated_module.is_multiply_prime

# There is no collection-valued "empty" case in this integer contract. Zero is
# included as the neutral/boundary integer analogue. These named witnesses cover
# every source-level branch outcome and the documented example.
named_inputs = {
    "large_negative": -1_000_000_007,
    "negative_one": -1,
    "zero_boundary": 0,
    "one_boundary": 1,
    "smallest_prime": 2,
    "loop_initially_false_prime": 3,
    "first_loop_entry_divisible": 4,
    "loop_remainder_else": 5,
    "before_first_true": 7,
    "repeated_factor_true": 8,
    "two_factors_false": 9,
    "three_factors_repeated": 12,
    "prime_cube_true": 27,
    "documented_example": 30,
    "distinct_factors_true": 42,
    "largest_below_bound_true": 99,
}

rng = random.Random(750075)
generated_negatives = {rng.randint(-10**12, -129) for _ in range(256)}
inputs = sorted(set(range(-128, 100)) | set(named_inputs.values()) | generated_negatives)

mismatches: list[tuple[int, bool, bool, bool]] = []
for value in inputs:
    canonical_result = canonical(value)
    generated_result = generated(value)
    math_result = independent_three_prime_factors(value)
    if not isinstance(canonical_result, bool) or not isinstance(generated_result, bool):
        raise AssertionError(
            f"non-Boolean result for {value}: "
            f"canonical={canonical_result!r}, generated={generated_result!r}"
        )
    if canonical_result != generated_result or generated_result != math_result:
        mismatches.append(
            (value, canonical_result, generated_result, math_result)
        )

print("contract: integer a < 100; no collection/empty input case exists")
print(f"input_count={len(inputs)}")
print(f"contiguous_range=-128..99 ({len(range(-128, 100))} inputs)")
print(f"deterministic_generated_negative_count={len(generated_negatives)}")
print("named_branch_and_boundary_results:")
for label, value in named_inputs.items():
    print(
        f"  {label}: a={value}, canonical={canonical(value)}, "
        f"generated={generated(value)}, math={independent_three_prime_factors(value)}"
    )
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch}")

raise SystemExit(1 if mismatches else 0)
