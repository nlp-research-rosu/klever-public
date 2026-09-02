#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for triangle_area."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import random
from typing import Any, Callable


def load_function(path: Path) -> Callable[[Any, Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def outcome(function: Callable[..., Any], case: tuple[Any, Any, Any]) -> tuple[str, Any]:
    try:
        value = function(*case)
    except Exception as error:  # Differential comparison includes exceptions.
        return ("exception", type(error).__name__)
    if isinstance(value, float) and math.isnan(value):
        return ("value", "NaN")
    return ("value", value)


canonical = load_function(Path("/tmp/audit-work/reference/canonical.py"))
generated = load_function(Path("/tmp/audit-work/candidate-fresh/solution.py"))

# Named cases cover both examples, no iterable/empty input (the API is three
# required scalars), zero/negative lengths, equality at each guard, the first
# point after each equality boundary, and ordinary/scalene/equilateral paths.
named_cases: list[tuple[Any, Any, Any]] = [
    (3, 4, 5),
    (1, 2, 10),
    (0, 0, 0),
    (0, 1, 1),
    (-1, 2, 2),
    (1, 2, 3),      # first guard equality
    (1, 3, 2),      # second guard equality after first is false
    (3, 1, 2),      # third guard equality after first two are false
    (1, 2, 2),      # one integer step inside validity
    (2, 1, 2),
    (2, 2, 1),
    (5, 12, 13),
    (2, 2, 2),
    (0.1, 0.1, 0.2),
    (0.1, 0.1, 0.199999999999),
    (1.5, 2.5, 3.0),
]

small_integer_cases = [
    (a, b, c)
    for a in range(-3, 21)
    for b in range(-3, 21)
    for c in range(-3, 21)
]

float_grid = [-1.0, 0.0, 0.1, 0.5, 1.0, 1.25, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0]
float_cases = [(a, b, c) for a in float_grid for b in float_grid for c in float_grid]

rng = random.Random(710071)
random_cases = [
    tuple(round(rng.uniform(-10.0, 1000.0), 6) for _ in range(3))
    for _ in range(2000)
]

cases = named_cases + small_integer_cases + float_cases + random_cases
mismatches: list[tuple[tuple[Any, Any, Any], tuple[str, Any], tuple[str, Any]]] = []
for case in cases:
    expected = outcome(canonical, case)
    actual = outcome(generated, case)
    if expected != actual:
        mismatches.append((case, expected, actual))

print(f"named_cases={len(named_cases)}")
print(f"small_integer_cases={len(small_integer_cases)} range=-3..20 per coordinate")
print(f"float_grid_cases={len(float_cases)} grid={float_grid}")
print(f"random_cases={len(random_cases)} seed=710071 uniform=[-10,1000], rounded=6dp")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
