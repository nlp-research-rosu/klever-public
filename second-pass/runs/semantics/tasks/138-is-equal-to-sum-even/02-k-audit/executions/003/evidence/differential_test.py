#!/usr/bin/env python3
"""Independent differential test for HumanEval/138."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical")
generated = load(Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution")

documented = [4, 6, 8]
branch_boundaries = [-2, -1, 0, 1, 2, 5, 6, 7, 8, 9, 10, 11]
large_boundaries = [
    -(10**100),
    -(10**100) + 1,
    10**100,
    10**100 + 1,
    2**1024,
    2**1024 + 1,
]
exhaustive = list(range(-10_000, 10_001))
rng = random.Random(138)
generated_inputs = [rng.randint(-(10**30), 10**30) for _ in range(5_000)]
inputs = documented + branch_boundaries + large_boundaries + exhaustive + generated_inputs

mismatches = []
true_count = 0
false_count = 0
for n in inputs:
    expected = canonical.is_equal_to_sum_even(n)
    actual = generated.is_equal_to_sum_even(n)
    if actual:
        true_count += 1
    else:
        false_count += 1
    if type(actual) is not bool or actual != expected:
        mismatches.append((n, expected, actual, type(actual).__name__))

print("oracle=/reference/canonical.py:is_equal_to_sum_even")
print("subject=/tmp/audit-work/reconstruction/solution.py:is_equal_to_sum_even")
print(f"documented_examples={documented}")
print(f"branch_boundary_inputs={branch_boundaries}")
print(f"large_boundary_inputs={large_boundaries}")
print("exhaustive_integer_interval=[-10000,10000]")
print("generated_seed=138 generated_count=5000 generated_range=[-10**30,10**30]")
print(f"total_cases={len(inputs)} true_results={true_count} false_results={false_count}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"mismatch={mismatch!r}")
sys.exit(1 if mismatches else 0)
