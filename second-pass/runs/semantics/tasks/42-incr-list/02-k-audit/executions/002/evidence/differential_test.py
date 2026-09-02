#!/usr/bin/env python3
"""Independent differential tests for HumanEval/42 incr_list."""

from __future__ import annotations

import importlib.util
import json
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
candidate = load_module("generated_solution", Path("/candidate/solution.py"))

# Documented cases, loop boundaries, sign/addition boundaries, arbitrary-size
# integers, repeated values, and numeric-list cases admitted by plain Python.
cases: list[list[int | float | bool]] = [
    [1, 2, 3],
    [5, 3, 5, 2, 3, 3, 9, 0, 123],
    [],
    [0],
    [-1],
    [1],
    [-2, -1, 0, 1, 2],
    [7, 7, 7],
    [-(2**100), -1, 0, 2**100],
    [1.5, -2.25, 0.0],
    [False, True],
]

rng = random.Random(420042)
for length in range(17):
    cases.append([rng.randint(-10**12, 10**12) for _ in range(length)])
for _ in range(100):
    length = rng.randint(0, 40)
    cases.append([rng.randint(-10**50, 10**50) for _ in range(length)])

mismatches = []
for index, value in enumerate(cases):
    oracle_input = list(value)
    candidate_input = list(value)
    expected = canonical.incr_list(oracle_input)
    actual = candidate.incr_list(candidate_input)
    if actual != expected:
        mismatches.append(
            {
                "index": index,
                "input": repr(value),
                "expected": repr(expected),
                "actual": repr(actual),
            }
        )

summary = {
    "oracle": "/reference/canonical.py::incr_list",
    "candidate": "/candidate/solution.py::incr_list",
    "documented_cases": 2,
    "explicit_boundary_cases": 9,
    "generated_integer_cases": 117,
    "total_cases": len(cases),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
