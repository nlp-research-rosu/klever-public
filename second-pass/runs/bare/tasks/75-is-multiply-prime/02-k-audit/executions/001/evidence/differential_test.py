#!/usr/bin/env python3
"""Independent program/contract differential for HumanEval 75."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


def mathematical_oracle(value: int) -> bool:
    """Exactly three prime factors, counted with multiplicity."""
    if value < 2:
        return False
    remaining = value
    factor_count = 0
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            remaining //= divisor
            factor_count += 1
        divisor += 1
    if remaining > 1:
        factor_count += 1
    return factor_count == 3


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated_solution", Path("/tmp/audit-work/rebuild/solution.py")
)

# Complete nonnegative intended interval, numeric empty/zero case, distant
# negatives for the unbounded lower side of A < 100, and deterministic generated
# negatives. This contains every equality arm and both neighbors of each arm.
rng = random.Random(20260723)
documented_examples = [30]
empty_numeric_cases = [0]
domain_boundaries = [-(10**100), -1_000_000, -101, -100, -2, -1, 0, 1, 2, 7, 8, 98, 99]
complete_nonnegative_domain = list(range(0, 100))
representative_generated = [rng.randint(-1_000_000, 99) for _ in range(32)]
inputs = sorted(
    set(
        documented_examples
        + empty_numeric_cases
        + domain_boundaries
        + complete_nonnegative_domain
        + representative_generated
    )
)

mismatches: list[tuple[int, bool, bool, bool]] = []
true_values: list[int] = []
for value in inputs:
    canonical_result = canonical(value)
    generated_result = generated(value)
    oracle_result = mathematical_oracle(value)
    if canonical_result:
        true_values.append(value)
    if not (
        type(canonical_result) is bool
        and type(generated_result) is bool
        and canonical_result == generated_result == oracle_result
    ):
        mismatches.append(
            (value, canonical_result, generated_result, oracle_result)
        )

print("oracle=independent prime-factor-count implementation")
print("documented_examples=", documented_examples)
print("empty_numeric_cases=", empty_numeric_cases)
print("domain_boundaries=", domain_boundaries)
print("complete_nonnegative_domain=range(0,100)")
print("random_seed=20260723")
print("representative_generated=", representative_generated)
print("tested_input_count=", len(inputs))
print("tested_inputs=", inputs)
print("true_values=", true_values)
print("mismatch_count=", len(mismatches))
print("mismatches=", mismatches)

if mismatches:
    raise SystemExit(1)
