#!/usr/bin/env python3
"""Independent differential tests for HumanEval 62 derivative."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derivative


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/candidate/solution.py"), "candidate_solution")

documented_and_boundaries = [
    [3, 1, 2, 4, 5],
    [1, 2, 3],
    [],
    [0],
    [7],
    [-7],
    [0, 0],
    [5, -1],
    [0, -2, 5],
    [-3, -2, -1, 0, 1, 2, 3],
    [10**100, -(10**100), 2],
    list(range(-100, 101)),
]

coefficient_alphabet = (-3, -1, 0, 1, 2, 7)
generated_integer_inputs = (
    list(values)
    for length in range(0, 6)
    for values in itertools.product(coefficient_alphabet, repeat=length)
)

tested = 0
mismatches: list[tuple[list[object], object, object]] = []
for xs in itertools.chain(documented_and_boundaries, generated_integer_inputs):
    expected = canonical(xs)
    actual = generated(xs)
    tested += 1
    if expected != actual:
        mismatches.append((xs, expected, actual))

# The formal K claims use integers. These extra source-level probes document
# that the Python rewrite also agrees on representative non-integer numeric
# coefficients; they are evidence only and do not widen the formal theorem.
extra_numeric_inputs = [
    [1.5, -2.25, 0.0],
    [0.0],
    [1 + 2j, -3j, 4 - 5j],
]
for xs in extra_numeric_inputs:
    expected = canonical(xs)
    actual = generated(xs)
    tested += 1
    if expected != actual:
        mismatches.append((xs, expected, actual))

print("oracle=/reference/canonical.py:derivative")
print("subject=/candidate/solution.py:derivative")
print("documented_and_boundary_cases=12")
print("generated_scope=all lengths 0..5 over coefficients (-3,-1,0,1,2,7)")
print("generated_integer_case_count=9331")
print("extra_numeric_case_count=3")
print(f"total_case_count={tested}")
print(f"mismatch_count={len(mismatches)}")
for xs, expected, actual in mismatches[:20]:
    print(f"MISMATCH input={xs!r} canonical={expected!r} generated={actual!r}")

if canonical([3, 1, 2, 4, 5]) != [1, 4, 12, 20]:
    raise AssertionError("trusted canonical disagrees with documented example 1")
if canonical([1, 2, 3]) != [2, 6]:
    raise AssertionError("trusted canonical disagrees with documented example 2")
raise SystemExit(1 if mismatches else 0)
