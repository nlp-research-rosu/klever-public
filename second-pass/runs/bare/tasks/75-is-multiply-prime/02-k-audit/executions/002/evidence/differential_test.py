#!/usr/bin/env python3
"""Differential and independent-oracle checks for HumanEval/75."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


def is_prime_independent(n: int) -> bool:
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def mathematical_oracle(a: int) -> bool:
    """Existence of p*q*r=a for primes p,q,r, independently enumerated."""
    if a < 8:
        return False
    for p in range(2, a + 1):
        if not is_prime_independent(p):
            continue
        for q in range(p, a + 1):
            if not is_prime_independent(q):
                continue
            pq = p * q
            if pq > a:
                break
            if a % pq == 0:
                r = a // pq
                if r >= q and is_prime_independent(r) and pq * r == a:
                    return True
    return False


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/candidate/solution.py"), "candidate_solution")

true_branches = [
    8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50,
    52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99,
]
documented_and_boundary = [30, 0, -1, 1, 2, 7, 8, 9, 98, 99]
branch_boundaries = sorted(
    {value + offset for value in true_branches for offset in (-1, 0, 1)}
)
rng = random.Random(750075)
generated_sample = [rng.randint(-10**9, 99) for _ in range(40)]
exhaustive_small = list(range(-250, 100))
inputs = sorted(
    set(documented_and_boundary + branch_boundaries + generated_sample + exhaustive_small)
)

mismatches = []
oracle_mismatches = []
for value in inputs:
    expected = canonical(value)
    actual = generated(value)
    oracle = mathematical_oracle(value)
    if expected != actual:
        mismatches.append((value, expected, actual))
    if expected != oracle or actual != oracle:
        oracle_mismatches.append((value, expected, actual, oracle))

print("documented_and_boundary", documented_and_boundary)
print("true_branch_values", true_branches)
print("branch_boundary_count", len(branch_boundaries))
print("generated_seed", 750075)
print("generated_sample", generated_sample)
print("complete_input_count", len(inputs))
print("complete_input_min", min(inputs))
print("complete_input_max", max(inputs))
print("canonical_candidate_mismatches", len(mismatches))
print("independent_oracle_mismatches", len(oracle_mismatches))
if mismatches:
    print("mismatch_details", mismatches)
if oracle_mismatches:
    print("oracle_mismatch_details", oracle_mismatches)

assert not mismatches
assert not oracle_mismatches
