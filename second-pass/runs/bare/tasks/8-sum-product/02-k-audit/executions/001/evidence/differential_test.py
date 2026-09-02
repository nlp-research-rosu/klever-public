#!/usr/bin/env python3
"""Independent differential test for HumanEval 8-sum-product."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/source/solution.py")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical_sum_product = load_entry("trusted_canonical", CANONICAL_PATH)
generated_sum_product = load_entry("audited_generated", GENERATED_PATH)

documented = [
    [],
    [1, 2, 3, 4],
]

boundaries = [
    [0],
    [1],
    [-1],
    [2],
    [-2],
    [0, 0],
    [1, 0],
    [0, 1],
    [-2, 0, 5],
    [2, -3],
    [-(10**100), 10**100],
    [10**100, 10**100, -(10**100)],
]

alphabet = (-3, -1, 0, 1, 2, 4)
exhaustive = [
    list(values)
    for length in range(0, 6)
    for values in itertools.product(alphabet, repeat=length)
]

rng = random.Random(8008)
generated = [
    [rng.randint(-(10**6), 10**6) for _ in range(rng.randint(0, 32))]
    for _ in range(500)
]

cases = documented + boundaries + exhaustive + generated
mismatches = []
for index, numbers in enumerate(cases):
    canonical_result = canonical_sum_product(numbers)
    generated_result = generated_sum_product(numbers)
    if canonical_result != generated_result:
        mismatches.append(
            (index, numbers, canonical_result, generated_result)
        )

print(f"canonical={CANONICAL_PATH}")
print(f"generated={GENERATED_PATH}")
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(
    "exhaustive_cases="
    f"{len(exhaustive)} alphabet={alphabet} lengths=0..5"
)
print("generated_cases=500 seed=8008 length=0..32 values=-1000000..1000000")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
