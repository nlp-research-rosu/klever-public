#!/usr/bin/env python3
"""Independent differential test for HumanEval 145.

Oracle: trusted /reference/canonical.py.
Implementation: clean scratch copy of the submitted solution.py.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


oracle = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module(
    "scratch_candidate",
    Path("/tmp/audit-work/145-order-by-points/solution.py"),
)

documented_and_boundary_cases = [
    [1, 11, -1, -11, -12],
    [],
    [0],
    [-1],
    [1],
    [-10, -1, 0, 1, 10],
    [99, -123, 8, 80, -9],
    [0, -10, 100, 2, -2, 20],
    [10, 1, 100, 1000],
    [-10, -1, -100, -1000],
    [11, 2, 20, 101, -11, -2, -20, -101],
    [7, 7, -7, -7, 7],
    [10**100, -(10**100), 10**100 - 1, -(10**100 - 1)],
]

pool = [
    -1000,
    -999,
    -123,
    -100,
    -99,
    -12,
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
    12,
    99,
    100,
    123,
    999,
    1000,
]

cases = list(documented_and_boundary_cases)
for length in range(4):
    cases.extend(list(values) for values in itertools.product(pool, repeat=length))

rng = random.Random(145)
for _ in range(5000):
    length = rng.randrange(0, 31)
    values = []
    for _ in range(length):
        mode = rng.randrange(4)
        if mode == 0:
            values.append(rng.choice(pool))
        elif mode == 1:
            values.append(rng.randrange(-10**6, 10**6 + 1))
        elif mode == 2:
            exponent = rng.randrange(0, 101)
            values.append(rng.choice((-1, 1)) * (10**exponent + rng.randrange(10)))
        else:
            values.append(rng.randrange(-200, 201))
    cases.append(values)

mismatches = []
for index, values in enumerate(cases):
    expected = oracle.order_by_points(list(values))
    actual = candidate.order_by_points(list(values))
    if actual != expected:
        mismatches.append((index, values, expected, actual))
        if len(mismatches) == 10:
            break

print("oracle=/reference/canonical.py:order_by_points")
print("implementation=/tmp/audit-work/145-order-by-points/solution.py:order_by_points")
print(f"documented_and_boundary_cases={len(documented_and_boundary_cases)}")
print(f"exhaustive_pool_size={len(pool)}")
print("exhaustive_lengths=0..3")
print("random_seed=145 random_cases=5000 random_lengths=0..30")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH={mismatch!r}")

raise SystemExit(1 if mismatches else 0)
