#!/usr/bin/env python3
"""Independent finite differential check for HumanEval/55 over its nonnegative domain."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib


def independent_iterative_fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(Path("/candidate/solution.py"), "generated_solution")

documented_examples = [10, 1, 8]
branch_boundaries = [0, 1, 2]
rng = random.Random(5500)
representative_generated = [rng.randrange(0, 23) for _ in range(12)]
inputs = sorted(set(documented_examples + branch_boundaries + list(range(0, 13)) + representative_generated))

mismatches = []
for n in inputs:
    expected = independent_iterative_fib(n)
    canonical_value = canonical(n)
    generated_value = generated(n)
    row = (n, canonical_value, generated_value, expected)
    print(f"n={n:2d} canonical={canonical_value:5d} generated={generated_value:5d} iterative={expected:5d}")
    if not (canonical_value == generated_value == expected):
        mismatches.append(row)

print(f"documented_examples={documented_examples}")
print(f"branch_boundaries={branch_boundaries}")
print(f"representative_generated={representative_generated}")
print(f"tested_inputs={inputs}")
print("empty_case=NOT_APPLICABLE_scalar_integer_argument")
print(f"mismatch_count={len(mismatches)}")
assert not mismatches, mismatches
