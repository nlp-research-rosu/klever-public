#!/usr/bin/env python3
"""Independent canonical-vs-generated differential for HumanEval/0."""

from __future__ import annotations

from itertools import combinations, product
import importlib.util
import math
from pathlib import Path
import random
import sys


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


canonical = load_function("trusted_canonical", "/reference/canonical.py")
generated = load_function("submitted_generated", "/candidate/solution.py")


def independent_oracle(numbers: list[float], threshold: float) -> bool:
    return any(abs(left - right) < threshold for left, right in combinations(numbers, 2))


explicit_cases = [
    # Documented examples.
    ([1.0, 2.0, 3.0], 0.5),
    ([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
    # Empty/singleton and loop-entry boundaries.
    ([], 0.5),
    ([1.0], 0.5),
    # i < j false/true paths, distance false/true paths, and sticky `found`.
    ([0.0, 2.0], 1.0),
    ([0.0, 0.25], 1.0),
    ([0.0, 10.0, 10.25], 0.5),
    ([0.0, 0.25, 10.0], 0.5),
    # Strict-comparison boundary and its immediate neighbors.
    ([1.0, 1.5], 0.5),
    ([1.0, 1.5], math.nextafter(0.5, math.inf)),
    ([1.0, 1.5], math.nextafter(0.5, -math.inf)),
    # Zero, negative thresholds, duplicates, signed zero, and ordering.
    ([1.0, 1.0], 0.0),
    ([1.0, 1.0], math.nextafter(0.0, math.inf)),
    ([1.0, 1.0], -1.0),
    ([-0.0, 0.0], math.nextafter(0.0, math.inf)),
    ([2.0, 0.0, 1.0], 1.5),
    # Representative IEEE special values accepted by CPython's float type.
    ([math.inf, math.inf], 1.0),
    ([-math.inf, math.inf], math.inf),
    ([math.nan, 0.0], 1.0),
    ([sys.float_info.max, math.nextafter(sys.float_info.max, 0.0)], math.inf),
]

grid_values = [-2.0, -0.5, -0.0, 0.5, 2.0]
grid_thresholds = [-1.0, 0.0, 0.25, 0.5, 1.0, 3.0]
grid_cases = [
    (list(numbers), threshold)
    for size in range(5)
    for numbers in product(grid_values, repeat=size)
    for threshold in grid_thresholds
]

rng = random.Random(0x0C105E)
sample_values = [
    -1e300,
    -100.0,
    -1.0,
    -1e-300,
    -0.0,
    0.0,
    1e-300,
    0.125,
    1.0,
    100.0,
    1e300,
]
sample_thresholds = [
    -1e300,
    -1.0,
    -0.0,
    0.0,
    math.nextafter(0.0, math.inf),
    1e-300,
    0.125,
    1.0,
    1e300,
    math.inf,
]
random_cases = [
    (
        [rng.choice(sample_values) for _ in range(rng.randrange(0, 13))],
        rng.choice(sample_thresholds),
    )
    for _ in range(2000)
]

all_cases = explicit_cases + grid_cases + random_cases
mismatches = []
for index, (numbers, threshold) in enumerate(all_cases):
    original = list(numbers)
    expected = canonical(list(numbers), threshold)
    actual = generated(list(numbers), threshold)
    oracle = independent_oracle(list(numbers), threshold)
    if expected is not oracle or actual is not expected:
        mismatches.append((index, numbers, threshold, expected, actual, oracle))
    unchanged = len(numbers) == len(original) and all(
        left is right or left == right for left, right in zip(numbers, original)
    )
    if not unchanged:
        mismatches.append((index, "INPUT_MUTATED", original, numbers))

print("COMMAND: python3 /audit-output/evidence/02_differential.py")
print("ORACLES: trusted /reference/canonical.py and independent itertools.combinations")
print("EXPLICIT_CASES:", len(explicit_cases))
print(
    "GRID:",
    "sizes=0..4",
    f"values={grid_values!r}",
    f"thresholds={grid_thresholds!r}",
    f"cases={len(grid_cases)}",
)
print(
    "RANDOM:",
    "seed=0x0C105E",
    "sizes=0..12",
    f"values={sample_values!r}",
    f"thresholds={sample_thresholds!r}",
    f"cases={len(random_cases)}",
)
print("TOTAL_CASES:", len(all_cases))
print("MISMATCHES:", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))
print("SCRIPT_EXIT=" + ("1" if mismatches else "0"))
raise SystemExit(1 if mismatches else 0)
