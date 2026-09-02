#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval 70."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/task70")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_70", ROOT / "canonical.py").strange_sort_list
generated = load("generated_solution_70", ROOT / "solution.py").strange_sort_list

documented_and_boundaries = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 2, 3],
    [3, 2, 1],
    [1, 2, 3, 4],
    [5, 5, 5, 5],
    [-1, 3, 0, 3, 2],
    [-10**100, 0, 10**100],
    [10**100, -10**100, 7, 7],
    [0, -1, -1, 0, 1, 1],
]

checked = 0


def check(values: list[int], label: str) -> None:
    global checked
    canonical_input = list(values)
    generated_input = list(values)
    expected = canonical(canonical_input)
    actual = generated(generated_input)
    if actual != expected:
        raise AssertionError(
            f"{label}: input={values!r} canonical={expected!r} generated={actual!r}"
        )
    if generated_input != values:
        raise AssertionError(f"{label}: generated implementation mutated its argument")
    checked += 1


for index, values in enumerate(documented_and_boundaries):
    check(values, f"documented/boundary[{index}]")
    print(f"case[{index}] input={values!r} output={generated(list(values))!r}")

alphabet = (-2, -1, 0, 1, 2)
exhaustive = 0
for length in range(7):
    for values in itertools.product(alphabet, repeat=length):
        check(list(values), f"exhaustive length={length}")
        exhaustive += 1

rng = random.Random(0x70)
random_count = 5000
for index in range(random_count):
    length = rng.randrange(0, 65)
    values = [rng.randint(-(10**12), 10**12) for _ in range(length)]
    check(values, f"random[{index}]")

print(
    "PASS "
    f"documented_and_boundaries={len(documented_and_boundaries)} "
    f"exhaustive={exhaustive} alphabet={alphabet} lengths=0..6 "
    f"random={random_count} random_lengths=0..64 seed=0x70 "
    f"total={checked} mismatches=0"
)
