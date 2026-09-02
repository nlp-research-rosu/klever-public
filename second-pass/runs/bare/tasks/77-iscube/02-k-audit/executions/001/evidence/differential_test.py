#!/usr/bin/env python3
"""Independent differential and exact-contract checks for HumanEval/77."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path

CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/77-iscube/candidate-src/solution.py")


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.iscube


canonical_iscube = load_entry("trusted_canonical", CANONICAL)
generated_iscube = load_entry("generated_solution", GENERATED)


def exact_iscube(a: int) -> bool:
    """Independent integer oracle using binary search, not candidate logic."""
    magnitude = abs(a)
    lo, hi = 0, 1
    while hi * hi * hi < magnitude:
        hi *= 2
    while lo <= hi:
        mid = (lo + hi) // 2
        cube = mid * mid * mid
        if cube == magnitude:
            return True
        if cube < magnitude:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


documented = [1, 2, -1, 64, 0, 180]
branch_boundaries = [
    -65,
    -64,
    -63,
    -28,
    -27,
    -26,
    -9,
    -8,
    -7,
    -2,
    -1,
    0,
    1,
    2,
    7,
    8,
    9,
    26,
    27,
    28,
    63,
    64,
    65,
]
constructed = []
for root in list(range(0, 501)) + [999, 1000, 10_000, 100_000]:
    cube = root**3
    for delta in (-2, -1, 0, 1, 2):
        constructed.extend((cube + delta, -(cube + delta)))

rng = random.Random(770077)
generated_random = [rng.randint(-(10**9), 10**9) for _ in range(5000)]

cases = []
seen = set()
for value in (
    documented
    + branch_boundaries
    + list(range(-50_000, 50_001))
    + constructed
    + generated_random
):
    if value not in seen:
        seen.add(value)
        cases.append(value)

mismatches = []
oracle_mismatches = []
for value in cases:
    canonical_value = canonical_iscube(value)
    generated_value = generated_iscube(value)
    oracle_value = exact_iscube(value)
    if canonical_value != generated_value:
        mismatches.append((value, canonical_value, generated_value, oracle_value))
    if generated_value != oracle_value:
        oracle_mismatches.append((value, generated_value, oracle_value))

print(f"canonical={CANONICAL}")
print(f"generated={GENERATED}")
print("documented_inputs=" + repr(documented))
print("branch_boundary_inputs=" + repr(branch_boundaries))
print("exhaustive_range=[-50000,50000]")
print("constructed_roots=0..500,999,1000,10000,100000; deltas=+-{0,1,2}; both signs")
print("random_seed=770077 random_count=5000 random_range=[-1000000000,1000000000]")
print(f"unique_case_count={len(cases)}")
print(f"canonical_generated_mismatch_count={len(mismatches)}")
print(f"generated_exact_oracle_mismatch_count={len(oracle_mismatches)}")
if mismatches:
    print("canonical_generated_mismatches=" + repr(mismatches[:20]))
if oracle_mismatches:
    print("generated_exact_oracle_mismatches=" + repr(oracle_mismatches[:20]))

assert not mismatches, "canonical and generated differ in the recorded differential scope"
assert not oracle_mismatches, "generated result differs from the exact integer oracle"

