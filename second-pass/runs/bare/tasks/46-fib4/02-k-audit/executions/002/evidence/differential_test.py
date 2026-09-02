#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module("candidate_solution", Path("/candidate/solution.py"))

# The sequence contract indexes from zero; these cover every explicit return,
# the no-iteration loop boundary, the first iteration, all examples, a dense
# prefix, and a reproducible broader generated sample.
documented = [5, 6, 7]
branch_boundaries = [0, 1, 2, 3, 4, 5]
dense = list(range(0, 201))
rng = random.Random(460046)
generated = [rng.randrange(0, 501) for _ in range(100)]
inputs = list(dict.fromkeys(documented + branch_boundaries + dense + generated))

mismatches: list[tuple[int, object, object]] = []
for n in inputs:
    expected = canonical.fib4(n)
    actual = candidate.fib4(n)
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"documented={documented}")
print(f"branch_boundaries={branch_boundaries}")
print("dense_range=0..200 inclusive")
print(f"generated_seed=460046 generated_count={len(generated)} generated_range=0..500")
print(f"unique_test_count={len(inputs)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH n={mismatch[0]} canonical={mismatch[1]} candidate={mismatch[2]}")

# Negative indices are not sequence indices in the prompt's n-th-element
# contract. Keep an exploratory record because Python's list indexing gives
# the canonical implementation incidental behavior for -1..-4.
for n in [-1, -2, -3, -4, -5]:
    try:
        expected: object = canonical.fib4(n)
    except Exception as error:  # noqa: BLE001 - evidence should record the exact class.
        expected = f"EXCEPTION:{type(error).__name__}"
    try:
        actual: object = candidate.fib4(n)
    except Exception as error:  # noqa: BLE001
        actual = f"EXCEPTION:{type(error).__name__}"
    print(f"exploratory_negative n={n} canonical={expected} candidate={actual}")

if mismatches:
    raise SystemExit(1)
