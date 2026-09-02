#!/usr/bin/env python3
"""Independent CPython differential audit for HumanEval 151.

The zero-mismatch primary domain is arbitrary-size Python ints and finite
Python floats, matching the candidate proof's Int/Float sequence domain.
Additional Python numeric edge types are reported separately so that any
source-contract interpretation issue remains visible.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.double_the_difference


canonical = load_function(ROOT / "canonical.py", "audit_canonical")
generated = load_function(ROOT / "solution.py", "audit_generated")


def same(left, right) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        if math.isnan(left) and math.isnan(right):
            return True
    return left == right and type(left) is type(right)


def compare(cases, label: str):
    mismatches = []
    total = 0
    for values in cases:
        total += 1
        try:
            expected = canonical(values)
            expected_exc = None
        except Exception as err:  # preserved as differential evidence
            expected = None
            expected_exc = (type(err).__name__, str(err))
        try:
            actual = generated(values)
            actual_exc = None
        except Exception as err:  # preserved as differential evidence
            actual = None
            actual_exc = (type(err).__name__, str(err))
        if expected_exc != actual_exc or (
            expected_exc is None and not same(expected, actual)
        ):
            mismatches.append((values, expected, expected_exc, actual, actual_exc))
    print(f"{label}: cases={total} mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"  MISMATCH {mismatch!r}")
    return mismatches


documented_and_boundaries = [
    [1, 3, 2, 0],
    [-1, -2, 0],
    [9, -2],
    [0],
    [],
    [-3, -2, -1, 0, 1, 2, 3],
    [-3.0, -2.0, -1.0, -0.0, 0.0, 1.0, 2.0, 3.0],
    [3.0, 3, -5, 2.5, 7],
    [-(10**100), 10**100, 10**100 + 1],
    [-(10**1001) - 1, 10**1001 + 1],
    [True, False, 1, 0],
    [float("nan"), -0.0, 0.0],
]

primary_atoms = [-3, -2, -1, 0, 1, 2, 3, -2.5, 0.0, 2.5]
exhaustive = (
    list(items)
    for length in range(5)
    for items in itertools.product(primary_atoms, repeat=length)
)

rng = random.Random(151)
randomized = []
for _ in range(5000):
    values = []
    for _ in range(rng.randrange(0, 21)):
        if rng.randrange(4):
            bits = rng.randrange(0, 513)
            value = rng.getrandbits(bits)
            if rng.randrange(2):
                value = -value
        else:
            value = rng.uniform(-1.0e12, 1.0e12)
        values.append(value)
    randomized.append(values)

special_python_numeric_edges = [
    [float("inf")],
    [float("-inf")],
    [1, float("inf"), 3],
    [3 + 0j],
    [3 + 4j],
]

primary_mismatches = []
primary_mismatches += compare(documented_and_boundaries, "documented_and_boundaries")
primary_mismatches += compare(exhaustive, "exhaustive_lengths_0_through_4")
primary_mismatches += compare(randomized, "deterministic_randomized")
special_mismatches = compare(special_python_numeric_edges, "reported_special_edges")

print(f"PRIMARY_TOTAL_MISMATCHES={len(primary_mismatches)}")
print(f"SPECIAL_EDGE_MISMATCHES={len(special_mismatches)}")
raise SystemExit(1 if primary_mismatches else 0)
