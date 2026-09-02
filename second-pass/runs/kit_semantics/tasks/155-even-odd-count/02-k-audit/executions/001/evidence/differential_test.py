#!/usr/bin/env python3
"""Independent CPython differential and contract-property test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/155-even-odd-count")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


canonical = load_function("trusted_canonical", ROOT / "trusted/canonical.py")
generated = load_function("submitted_solution", ROOT / "work/solution.py")

documented = [(-12, (1, 1)), (123, (1, 2))]
branch_boundaries = [
    -1001,
    -1000,
    -999,
    -110,
    -109,
    -101,
    -100,
    -99,
    -20,
    -19,
    -11,
    -10,
    -9,
    -2,
    -1,
    0,
    1,
    2,
    9,
    10,
    11,
    19,
    20,
    99,
    100,
    101,
    109,
    110,
    999,
    1000,
    1001,
]
exhaustive = list(range(-100_000, 100_001))
random_source = random.Random(155)
generated_inputs: list[int] = []
for _ in range(2_000):
    digits = random_source.randint(1, 100)
    magnitude = random_source.randrange(10 ** (digits - 1), 10**digits)
    generated_inputs.append(
        -magnitude if random_source.randrange(2) else magnitude
    )

for value, expected in documented:
    assert canonical(value) == expected
    assert generated(value) == expected

all_inputs = branch_boundaries + exhaustive + generated_inputs
mismatches = []
property_failures = []
for value in all_inputs:
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append((value, expected, actual))
    digits = str(abs(value))
    direct = (
        sum(int(character) % 2 == 0 for character in digits),
        sum(int(character) % 2 == 1 for character in digits),
    )
    if actual != direct or sum(actual) != len(digits):
        property_failures.append((value, direct, actual))

print("documented_cases=2")
print(f"branch_boundary_cases={len(branch_boundaries)}")
print("exhaustive_integer_range=[-100000,100000]")
print("random_seed=155")
print("random_big_integer_cases=2000 digits=[1,100]")
print(f"total_comparisons={len(all_inputs) + len(documented)}")
print(f"mismatches={len(mismatches)}")
print(f"direct_contract_property_failures={len(property_failures)}")
if mismatches:
    print(f"first_mismatch={mismatches[0]}")
if property_failures:
    print(f"first_property_failure={property_failures[0]}")
assert not mismatches
assert not property_failures
