#!/usr/bin/env python3
"""Independent docstring/canonical differential for HumanEval 34."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/review-34-unique")


def load_function(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique


candidate = load_function(SCRATCH / "solution.py", "audited_candidate_solution")
canonical = load_function(SCRATCH / "trusted-canonical.py", "trusted_canonical_solution")


def normalized(value: Any) -> Any:
    if isinstance(value, float) and math.isnan(value):
        return ("NaN",)
    if isinstance(value, list):
        return ("list", tuple(normalized(item) for item in value))
    if isinstance(value, tuple):
        return ("tuple", tuple(normalized(item) for item in value))
    return (type(value).__name__, value)


def outcome(function: Callable[[list[Any]], list[Any]], case: list[Any]) -> tuple[Any, ...]:
    try:
        return ("return", normalized(function(case.copy())))
    except Exception as error:  # evidence compares exception class, not messages
        return ("raise", type(error).__name__)


documented = [[5, 3, 5, 2, 3, 3, 9, 0, 123]]
boundaries = [
    [],
    [1],
    [1, 1],
    [2, 1],
    [1, 2, 1],
    [-1, 0, -1],
    ["b", "a", "b", "c", "a"],
    [True, 1],
    [1, True],
    [False, 0, 2],
    [3.0, 2, 2.0, 3],
    [-0.0, 0.0, 1.0],
    [(2,), (1,), (2,)],
    [[2], [1], [2]],  # canonical rejects unhashable elements; docstring is silent
    [1, "1"],  # both reject mutually unorderable values; docstring is silent
]

exhaustive_ints = [
    list(items)
    for length in range(6)
    for items in itertools.product((-2, -1, 0, 1, 2), repeat=length)
]
exhaustive_strings = [
    list(items)
    for length in range(5)
    for items in itertools.product(("a", "b", "c"), repeat=length)
]

rng = random.Random(340034)
generated = [
    [rng.randint(-100, 100) for _ in range(rng.randint(0, 30))]
    for _ in range(1000)
]

cases = documented + boundaries + exhaustive_ints + exhaustive_strings + generated
mismatches: list[tuple[int, list[Any], tuple[Any, ...], tuple[Any, ...]]] = []
for index, case in enumerate(cases):
    expected = outcome(canonical, case)
    actual = outcome(candidate, case)
    if expected != actual:
        mismatches.append((index, case, expected, actual))

print("CONTRACT: Return the elements of the input list once each, in ascending sorted order.")
print(f"DOCUMENTED_CASES={len(documented)}")
print(f"BOUNDARY_CASES={len(boundaries)}")
print(f"EXHAUSTIVE_INTEGER_CASES={len(exhaustive_ints)}")
print(f"EXHAUSTIVE_STRING_CASES={len(exhaustive_strings)}")
print(f"SEEDED_RANDOM_CASES={len(generated)}")
print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCHES={len(mismatches)}")
for index, case, expected, actual in mismatches[:50]:
    print(f"MISMATCH index={index} case={case!r} canonical={expected!r} candidate={actual!r}")

example_actual = candidate(documented[0].copy())
print(f"DOCUMENTED_EXAMPLE_RESULT={example_actual!r}")
assert example_actual == [0, 2, 3, 5, 9, 123]

# Direct property checks avoid making canonical equality the contract.
property_cases = documented + boundaries[:13] + exhaustive_ints + exhaustive_strings + generated
for case in property_cases:
    result = candidate(case.copy())
    assert result == sorted(result), (case, result)
    for item in case:
        assert item in result, (case, result, item)
    assert all(result.count(item) == 1 for item in result), (case, result)
print(f"DOCSTRING_PROPERTY_CASES={len(property_cases)}")
print("DOCSTRING_PROPERTY_FAILURES=0")

