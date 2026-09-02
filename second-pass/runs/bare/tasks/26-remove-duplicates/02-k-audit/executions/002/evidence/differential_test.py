#!/usr/bin/env python3
"""Independent source-level differential test for HumanEval/26."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


canonical = load_entry(
    Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical"
)
candidate = load_entry(
    Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_solution"
)

documented_and_boundary = [
    [1, 2, 3, 2, 4],
    [],
    [0],
    [1, 1],
    [1, 1, 1],
    [1, 2],
    [1, 2, 1],
    [1, 2, 2],
    [1, 2, 1, 2],
    [-1, 0, -1, 2],
    [10**100, -(10**100), 10**100, 7],
    [3, 1, 3, 2, 1, 4, 2, 5],
]

inputs: list[list[int]] = list(documented_and_boundary)
for length in range(7):
    inputs.extend(
        list(values)
        for values in itertools.product(range(-2, 3), repeat=length)
    )

rng = random.Random(260726)
for _ in range(1000):
    length = rng.randrange(0, 41)
    inputs.append([rng.randrange(-20, 21) for _ in range(length)])

mismatches: list[tuple[list[int], list[int], list[int]]] = []
for values in inputs:
    expected = canonical(list(values))
    actual = candidate(list(values))
    if actual != expected:
        mismatches.append((values, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_and_boundary_cases={len(documented_and_boundary)}")
print("exhaustive_domain=all lists of lengths 0..6 over integers -2..2")
print("random_domain=1000 deterministic lists of lengths 0..40 over -20..20")
print(f"total_cases={len(inputs)}")
print(f"mismatch_count={len(mismatches)}")
for values, expected, actual in mismatches:
    print(f"MISMATCH input={values!r} canonical={expected!r} candidate={actual!r}")

if mismatches:
    raise SystemExit(1)
