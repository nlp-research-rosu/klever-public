#!/usr/bin/env python3
"""Independent result differential for HumanEval/70.

The trusted canonical function mutates its argument, so every implementation
receives a distinct copy.  The test compares returned values only because the
source contract specifies only the return value.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work")
CANONICAL_PATH = ROOT / "trusted" / "canonical.py"
GENERATED_PATH = ROOT / "clean-candidate" / "solution.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", CANONICAL_PATH).strange_sort_list
generated = load_module("candidate_solution", GENERATED_PATH).strange_sort_list


documented = [
    [1, 2, 3, 4],
    [5, 5, 5, 5],
    [],
]

# Explicitly hit both base branches and both odd/even recursive shapes.
boundaries = [
    [0],
    [-1],
    [2, 1],
    [1, 2],
    [2, 2],
    [3, 1, 2],
    [4, 1, 3, 2],
    [4, 1, 7, 2, 6],
    [3, -1, 2, 3, 0],
    [-10, 10, 0, -10, 10, 5],
]

# Exhaust all lists up to length 6 over a small integer alphabet.
exhaustive = [
    list(values)
    for length in range(7)
    for values in itertools.product(range(-2, 3), repeat=length)
]

# Add broader deterministic samples with duplicates, signs, and larger values.
rng = random.Random(70070)
random_cases = [
    [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 30))]
    for _ in range(2000)
]

cases = documented + boundaries + exhaustive + random_cases
mismatches: list[tuple[list[int], list[int], list[int]]] = []
for original in cases:
    expected = canonical(list(original))
    actual = generated(list(original))
    if actual != expected:
        mismatches.append((original, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_cases={len(exhaustive)} lengths=0..6 values=-2..2")
print(f"random_cases={len(random_cases)} seed=70070 lengths=0..30 values=-1000..1000")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for original, expected, actual in mismatches:
    print(f"MISMATCH input={original!r} canonical={expected!r} candidate={actual!r}")

raise SystemExit(1 if mismatches else 0)
