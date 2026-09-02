#!/usr/bin/env python3
"""Independent differential test for HumanEval/59.

The intended input domain is integer n > 1 with n composite. There is no
collection-valued "empty" input. The smallest domain boundary is n = 4.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
candidate = load_entry("/tmp/audit-work/59-lpf/solution.py", "candidate_solution")


def prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def independent_oracle(n: int) -> int:
    """Largest factor via descending search, independent of both algorithms."""
    for d in range(n // 2, 1, -1):
        if n % d == 0 and prime(d):
            return d
    return n


documented = [13195, 2048]
boundaries = [
    4,   # smallest allowed composite; divisible branch at factor 2
    6,   # divisible branch, then non-divisible increment branch
    8,   # repeated division by the same factor
    9,   # initial non-divisible branch, then division by factor 3
    10,  # even semiprime
    12,  # repeated and distinct factors
    15,  # odd semiprime
    25,  # odd prime square
    27,  # repeated odd factor
    49,  # square of a larger prime
]
exhaustive = [n for n in range(4, 5001) if not prime(n)]

rng = random.Random(590059)
primes = [n for n in range(2, 150) if prime(n)]
generated = [rng.choice(primes) * rng.choice(primes) for _ in range(250)]

inputs = sorted(set(documented + boundaries + exhaustive + generated))
mismatches = []
for n in inputs:
    assert n > 1 and not prime(n), f"generated off-domain input: {n}"
    expected = independent_oracle(n)
    canonical_result = canonical(n)
    candidate_result = candidate(n)
    if canonical_result != expected or candidate_result != expected:
        mismatches.append((n, expected, canonical_result, candidate_result))

print("domain: integers n > 1 that are not prime")
print("empty case: not applicable to this integer contract")
print("documented_examples:", documented)
print("branch_boundaries:", boundaries)
print("exhaustive_composites_4_through_5000:", len(exhaustive))
print("seeded_generated_products:", len(generated), "seed=590059")
print("unique_inputs:", len(inputs))
print("mismatches:", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)
raise SystemExit(1 if mismatches else 0)
