#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "canonical.py").below_zero
candidate = load("generated_solution", ROOT / "solution.py").below_zero

documented_and_boundaries = [
    [],
    [1, 2, 3],
    [1, 2, -4, 5],
    [0],
    [-1],
    [1],
    [1, -1],
    [1, -2],
    [0, -1],
    [5, -5],
    [5, -6],
    [-1, 100],
    [2, -1, -1],
    [2, -1, -2],
    [2, -1, -1, -1],
    [10**100, -(10**100)],
    [10**100, -(10**100) - 1],
    [-(10**100)],
]

cases: list[list[int]] = list(documented_and_boundaries)
for length in range(7):
    cases.extend(map(list, itertools.product(range(-3, 4), repeat=length)))

rng = random.Random(0x3B310)
special = [-(10**100), -(10**20), -2, -1, 0, 1, 2, 10**20, 10**100]
for _ in range(5000):
    length = rng.randrange(0, 51)
    case = [
        rng.choice(special) if rng.randrange(5) == 0 else rng.randrange(-10**6, 10**6)
        for _ in range(length)
    ]
    cases.append(case)

mismatches: list[tuple[list[int], object, object]] = []
true_count = 0
false_count = 0
for operations in cases:
    expected = canonical(list(operations))
    actual = candidate(list(operations))
    true_count += expected is True
    false_count += expected is False
    if expected != actual or type(expected) is not type(actual):
        mismatches.append((operations, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print("exhaustive_domain=lengths 0..6, elements -3..3")
print("random_domain=5000 seeded lists, lengths 0..50, mixed huge and ordinary ints")
print(f"total_cases={len(cases)}")
print(f"canonical_true_count={true_count}")
print(f"canonical_false_count={false_count}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"mismatch={mismatch!r}")
raise SystemExit(1 if mismatches else 0)
