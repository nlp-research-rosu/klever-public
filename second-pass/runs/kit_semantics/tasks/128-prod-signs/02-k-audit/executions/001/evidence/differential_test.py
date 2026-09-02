#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical")
generated = load(
    Path("/tmp/audit-work/128-prod-signs/solution.py"),
    "candidate_generated",
)

documented_and_boundaries = [
    [1, 2, 2, -4],
    [0, 1],
    [],
    [-1],
    [0],
    [1],
    [-1, -2],
    [-1, -2, -3],
    [-1, 0, 2],
    [2, 0, -1],
    [10**100],
    [-(10**100)],
    [10**100, -(10**100), 1],
]

cases = list(documented_and_boundaries)
alphabet = (-3, -1, 0, 1, 2)
for length in range(7):
    cases.extend([list(values) for values in itertools.product(alphabet, repeat=length)])

rng = random.Random(128)
for _ in range(10_000):
    length = rng.randrange(0, 31)
    values = []
    for _ in range(length):
        if rng.randrange(20) == 0:
            magnitude = rng.randrange(10**99, 10**100)
            values.append(magnitude if rng.randrange(2) else -magnitude)
        else:
            values.append(rng.randrange(-10_000, 10_001))
    cases.append(values)

mismatches = []
for index, values in enumerate(cases):
    expected = canonical.prod_signs(values)
    actual = generated.prod_signs(values)
    if actual != expected:
        mismatches.append((index, values, expected, actual))
        if len(mismatches) >= 20:
            break

print("ORACLE=/reference/canonical.py:prod_signs")
print("GENERATED=/tmp/audit-work/128-prod-signs/solution.py:prod_signs")
print(f"DOCUMENTED_BOUNDARY_CASES={len(documented_and_boundaries)}")
print("EXHAUSTIVE_DOMAIN=lengths_0_through_6 alphabet=-3,-1,0,1,2")
print("RANDOM_DOMAIN=seed_128 count_10000 lengths_0_through_30")
print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCHES={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", repr(mismatch))

raise SystemExit(1 if mismatches else 0)
