#!/usr/bin/env python3
"""Independent differential test for trusted and submitted Python entry points."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_function(ROOT / "reference" / "canonical.py", "trusted_canonical")
submitted = load_function(ROOT / "candidate" / "solution.py", "submitted_solution")

documented = [
    [1, 2, 3],
    [1, 4, 9],
    [1, 3, 5, 7],
    [1.4, 4.2, 0],
    [-2.4, 1, 1],
]

boundaries = [
    [],
    [0],
    [-0.0, 0.0],
    [-3, -2, -1, 0, 1, 2, 3],
    [-3.0000000000000004, -3.0, -2.9999999999999996],
    [-2.0000000000000004, -2.0, -1.9999999999999998],
    [-1.0000000000000002, -1.0, -0.9999999999999999],
    [-5e-324, 5e-324],
    [0.9999999999999999, 1.0, 1.0000000000000002],
    [2**53 - 1, 2**53, 2**53 + 1],
    [-(2**100), 2**100],
    [True, False],
]

rng = random.Random(133)
generated: list[list[int | float]] = []
for _ in range(2000):
    case: list[int | float] = []
    for _ in range(rng.randrange(13)):
        if rng.randrange(3) == 0:
            case.append(rng.randrange(-(10**9), 10**9 + 1))
        else:
            value = rng.uniform(-10**6, 10**6)
            if rng.randrange(4) == 0:
                value = math.nextafter(value, math.inf if rng.randrange(2) else -math.inf)
            case.append(value)
    generated.append(case)

cases = documented + boundaries + generated
mismatches = []
for index, case in enumerate(cases):
    try:
        expected = ("value", canonical(case))
    except Exception as error:  # pragma: no cover - retained for diagnostic parity
        expected = ("exception", type(error).__name__, str(error))
    try:
        actual = ("value", submitted(case))
    except Exception as error:  # pragma: no cover - retained for diagnostic parity
        actual = ("exception", type(error).__name__, str(error))
    if actual != expected:
        mismatches.append((index, case, expected, actual))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"generated_cases={len(generated)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))

raise SystemExit(1 if mismatches else 0)
