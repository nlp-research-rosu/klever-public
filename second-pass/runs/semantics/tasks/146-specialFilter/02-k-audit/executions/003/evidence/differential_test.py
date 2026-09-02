#!/usr/bin/env python3
"""Independent differential test for HumanEval 146-specialFilter."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/146-specialFilter")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


canonical = load_entry("trusted_canonical_146", SCRATCH / "canonical.py")
candidate = load_entry("candidate_solution_146", SCRATCH / "solution.py")


documented_and_boundary_cases = [
    [15, -73, 14, -15],
    [33, -2, -3, 45, 21, 109],
    [],
    [10],
    [11],
    [12],
    [19],
    [20],
    [21],
    [31],
    [99],
    [100],
    [101],
    [109],
    [111],
    [13579],
    [24681],
    [9990],
    [-11],
    [-999],
    [0, 1, 3, 5, 7, 9, 10, 11],
    [11, 13, 15, 17, 19, 21, 23, 25, 27, 29],
    [101, 103, 105, 107, 109, 201, 301, 401, 501],
]


cases = list(documented_and_boundary_cases)
cases.extend([[value] for value in range(-250, 5001)])

randomizer = random.Random(146)
for _ in range(2000):
    length = randomizer.randrange(0, 65)
    cases.append(
        [
            randomizer.randrange(-(10**30), 10**30)
            for _ in range(length)
        ]
    )

for index, nums in enumerate(cases):
    expected = canonical(list(nums))
    actual = candidate(list(nums))
    if expected != actual:
        print(
            f"MISMATCH index={index} input={nums!r} "
            f"canonical={expected!r} candidate={actual!r}"
        )
        raise SystemExit(1)

print(f"documented_and_boundary_cases={len(documented_and_boundary_cases)}")
print("exhaustive_singletons=-250..5000")
print("seed=146 random_lists=2000 lengths=0..64 values=[-10^30,10^30)")
print(f"total_cases={len(cases)} mismatches=0")
