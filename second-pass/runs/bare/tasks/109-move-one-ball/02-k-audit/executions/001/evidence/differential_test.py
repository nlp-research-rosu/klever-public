#!/usr/bin/env python3
"""Independent differential test of candidate solution against trusted canonical."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
import random
from typing import Callable


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/source/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential_inputs.json")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


canonical = load_entry(CANONICAL, "trusted_canonical")
generated = load_entry(GENERATED, "generated_solution")

documented_and_boundaries = [
    [],
    [0],
    [-7],
    [1, 2],
    [2, 1],
    [3, 4, 5, 1, 2],
    [3, 5, 4, 1, 2],
    [1, 2, 3, 4],
    [4, 1, 2, 3],
    [2, 1, 3],
    [3, 2, 1],
    [-3, -2, -1],
    [-1, -3, -2],
    [10**30, -(10**30), 0],
]

# Exhaust every permutation of distinct 0..n-1 for n=0..7: 5,914 inputs.
exhaustive = [
    list(values)
    for n in range(8)
    for values in itertools.permutations(range(n))
]

# Representative generated inputs include negative and very large values.
rng = random.Random(109)
random_cases: list[list[int]] = []
for _ in range(500):
    n = rng.randrange(0, 13)
    pool = rng.sample(range(-1000, 1001), n)
    if n and rng.randrange(5) == 0:
        pool[rng.randrange(n)] *= 10**20
    rng.shuffle(pool)
    random_cases.append(pool)

all_cases = documented_and_boundaries + exhaustive + random_cases
INPUT_RECORD.write_text(
    json.dumps(
        {
            "documented_and_boundaries": documented_and_boundaries,
            "exhaustive_definition": "all permutations(range(n)) for n=0..7",
            "exhaustive_count": len(exhaustive),
            "random_seed": 109,
            "random_count": len(random_cases),
            "random_cases": random_cases,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches: list[dict[str, object]] = []
for index, values in enumerate(all_cases):
    expected = canonical(values.copy())
    actual = generated(values.copy())
    if expected != actual:
        mismatches.append(
            {"index": index, "input": values, "canonical": expected, "generated": actual}
        )

for values in documented_and_boundaries:
    print(
        "EXPLICIT",
        json.dumps(values),
        f"canonical={canonical(values.copy())}",
        f"generated={generated(values.copy())}",
    )
print(f"CANONICAL={CANONICAL}")
print(f"GENERATED={GENERATED}")
print("EXHAUSTIVE_SCOPE=all permutations(range(n)) for n=0..7")
print(f"EXHAUSTIVE_COUNT={len(exhaustive)}")
print("RANDOM_SEED=109")
print(f"RANDOM_COUNT={len(random_cases)}")
print(f"TOTAL_COMPARISONS={len(all_cases)}")
print(f"MISMATCH_COUNT={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], indent=2))
    raise SystemExit(1)

