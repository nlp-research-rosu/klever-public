#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import inspect
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_fib(n: int) -> int:
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module("candidate_solution", Path("/candidate/solution.py"))

assert inspect.signature(candidate.fib) == inspect.signature(canonical.fib)

documented = [10, 1, 8]
boundaries = [0, 1, 2, 3]
exhaustive_small = list(range(0, 21))
rng = random.Random(550055)
generated = [rng.randrange(0, 31) for _ in range(20)]
inputs = list(dict.fromkeys(documented + boundaries + exhaustive_small + generated + [25, 30]))

mismatches: list[tuple[int, int, int, int]] = []
for n in inputs:
    expected = canonical.fib(n)
    actual = candidate.fib(n)
    oracle = independent_fib(n)
    print(f"n={n:2d} canonical={expected} candidate={actual} independent={oracle}")
    if not (expected == actual == oracle):
        mismatches.append((n, expected, actual, oracle))

print(f"documented={documented}")
print(f"boundaries={boundaries}")
print(f"generated_seed=550055 generated={generated}")
print(f"tested_unique_inputs={inputs}")
print(f"mismatch_count={len(mismatches)}")
assert not mismatches, mismatches
