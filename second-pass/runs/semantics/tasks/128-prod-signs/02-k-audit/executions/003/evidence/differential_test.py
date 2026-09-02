#!/usr/bin/env python3
"""Independent differential checks for HumanEval 128 prod_signs."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("candidate_solution", Path("/candidate/solution.py"))

documented = [
    [1, 2, 2, -4],
    [0, 1],
    [],
]
boundaries = [
    [0],
    [-1],
    [1],
    [-2, -3],
    [-2, 0, -3],
    [0, 0],
    [-10**100, 10**100],
    [-10**100, 0, 10**100],
]

cases: list[list[int]] = documented + boundaries
for length in range(7):
    cases.extend([list(values) for values in itertools.product(range(-3, 4), repeat=length)])

rng = random.Random(128)
specials = [-(10**100), -(2**63), -10, -1, 0, 1, 10, 2**63, 10**100]
for _ in range(10_000):
    length = rng.randrange(0, 41)
    values = [
        rng.choice(specials) if rng.randrange(5) == 0 else rng.randrange(-10_000, 10_001)
        for _ in range(length)
    ]
    cases.append(values)

mismatches: list[tuple[list[int], object, object]] = []
for values in cases:
    expected = canonical(list(values))
    actual = generated(list(values))
    if expected != actual or type(expected) is not type(actual):
        mismatches.append((values, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_cases={len(documented)}")
print(f"explicit_boundary_cases={len(boundaries)}")
print("exhaustive_domain=lengths_0_through_6_values_-3_through_3")
print("random_seed=128 random_cases=10000 lengths=0_through_40")
print(f"total_comparisons={len(cases) if not mismatches else 'stopped_early'}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH={mismatch!r}")

raise SystemExit(1 if mismatches else 0)
