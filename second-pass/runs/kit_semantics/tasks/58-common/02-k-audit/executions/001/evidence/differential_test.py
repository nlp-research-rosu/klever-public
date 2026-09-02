#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval/58."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/58-common")
SEED = 580058


def load_entry(module_name: str, path: Path) -> Callable[[list, list], list]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load_entry("trusted_canonical_58", SCRATCH / "canonical.py")
generated = load_entry("generated_solution_58", SCRATCH / "solution.py")


def outcome(function: Callable[[list, list], list], left: list, right: list) -> tuple:
    try:
        return ("value", function(left.copy(), right.copy()))
    except Exception as err:  # Compare specified failure behavior by exception class.
        return ("exception", type(err).__name__)


cases: list[tuple[str, list, list]] = [
    (
        "documented-example-1",
        [1, 4, 3, 34, 653, 2, 5],
        [5, 7, 1, 5, 9, 653, 121],
    ),
    ("documented-example-2", [5, 3, 2, 8], [3, 2]),
    ("both-empty", [], []),
    ("left-empty", [], [1]),
    ("right-empty", [1], []),
    ("singleton-miss", [1], [2]),
    ("singleton-hit", [1], [1]),
    ("condition-first-false", [1, 2], [2]),
    ("condition-first-true-second-true", [1, 1], [1]),
    ("condition-both-true", [2, 1], [1, 2]),
    ("duplicate-both-sides", [2, 2, 1, 1], [1, 2, 2]),
    ("reverse-needs-sort", [5, 4, 3, 2, 1], [5, 4, 3, 2, 1]),
    ("negative-and-large", [10**30, -10**30, 0], [0, 10**30, -10**30]),
    ("strings", ["z", "a", "z", "b"], ["b", "z"]),
    ("tuples", [(2,), (1,), (2,)], [(1,), (2,)]),
    ("booleans-and-ints", [True, 0, 1, False], [1, False]),
    ("finite-floats", [2.5, -1.0, 2.5], [-1.0, 2.5]),
    ("infinity", [float("inf"), -float("inf")], [float("inf")]),
    ("none-singleton", [None, None], [None]),
    ("shared-heterogeneous-sort-error", [1, "a"], ["a", 1]),
]

small_int_lists = [
    list(items)
    for size in range(4)
    for items in product((-2, -1, 0, 1, 2), repeat=size)
]
for left in small_int_lists:
    for right in small_int_lists:
        cases.append(("exhaustive-small-int", left, right))

small_string_lists = [
    list(items)
    for size in range(4)
    for items in product(("a", "b", "c"), repeat=size)
]
for left in small_string_lists:
    for right in small_string_lists:
        cases.append(("exhaustive-small-string", left, right))

rng = random.Random(SEED)
for _ in range(5000):
    left = [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 15))]
    right = [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 15))]
    cases.append(("seeded-random-int", left, right))

tuple_values = [(-2,), (0,), (1,), (1, 2)]
for _ in range(1000):
    left = [rng.choice(tuple_values) for _ in range(rng.randint(0, 10))]
    right = [rng.choice(tuple_values) for _ in range(rng.randint(0, 10))]
    cases.append(("seeded-random-tuple", left, right))

mismatches: list[tuple[Any, ...]] = []
category_counts: dict[str, int] = {}
exception_agreements = 0
for category, left, right in cases:
    category_counts[category] = category_counts.get(category, 0) + 1
    expected = outcome(canonical, left, right)
    actual = outcome(generated, left, right)
    if expected[0] == "exception" and actual == expected:
        exception_agreements += 1
    if actual != expected:
        mismatches.append((category, left, right, expected, actual))

print(f"seed={SEED}")
print(f"total_cases={len(cases)}")
print(f"category_counts={category_counts}")
print(f"matched_exception_cases={exception_agreements}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")
    raise AssertionError(f"{len(mismatches)} differential mismatches")
print("DIFFERENTIAL_TEST_COMPLETE")
