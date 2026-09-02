#!/usr/bin/env python3
"""Independent candidate-vs-canonical and mathematical-oracle comparison."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load("/tmp/audit-work/reconstruction/canonical.py", "trusted_canonical")
candidate = load("/tmp/audit-work/reconstruction/solution.py", "candidate_solution")


def oracle(values: list[int]) -> bool:
    return any(sum(triple) == 0 for triple in itertools.combinations(values, 3))


documented = [
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 9, 7],
    [1],
]
boundary = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [1, -1, 0],
    [1, -1, 2],
    [3, 0, -3, 99],
    [99, 3, 0, -3],
    [1, 1, -2],
    [1, 1, 1, -2],
    [10**80, -(10**80), 0],
    [10**80, 1, -(10**80)],
    [-7, -6, -5, 4, 8, 13],
]

rng = random.Random(4007)
generated: list[list[int]] = []
for length in range(0, 13):
    for _ in range(60):
        generated.append([rng.randint(-30, 30) for _ in range(length)])

# Exhaust every branch boundary over a small alphabet through the largest
# formally claimed length, plus one beyond the claim boundary.
exhaustive = [
    list(values)
    for length in range(0, 8)
    for values in itertools.product(range(-2, 3), repeat=length)
]
cases = documented + boundary + generated + exhaustive
mismatches = []
for index, values in enumerate(cases):
    expected = oracle(values)
    trusted_result = canonical(list(values))
    candidate_result = candidate(list(values))
    if not (expected == trusted_result == candidate_result):
        mismatches.append(
            (index, values, expected, trusted_result, candidate_result)
        )
        if len(mismatches) >= 20:
            break

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundary)}")
print(f"seeded_generated_cases={len(generated)} seed=4007 lengths=0..12")
print(f"exhaustive_cases={len(exhaustive)} lengths=0..7 alphabet=-2..2")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)
assert not mismatches
print("DIFFERENTIAL_STATUS=PASS")
