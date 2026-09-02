#!/usr/bin/env python3
"""Independent differential tests for HumanEval 135-can-arrange."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/reconstruction-135/solution.py")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


canonical = load(CANONICAL, "trusted_canonical_135")
generated = load(GENERATED, "generated_solution_135")


def outcome(function, value):
    try:
        return ("return", function(value))
    except BaseException as error:
        return ("raise", type(error).__name__, str(error))


def describe(value):
    if len(value) <= 12:
        return repr(value)
    return (
        f"len={len(value)} head={value[:4]!r} "
        f"tail={value[-4:]!r}"
    )


documented_and_branch_cases = [
    ("documented_drop", [1, 2, 4, 3, 5]),
    ("documented_sorted", [1, 2, 3]),
    ("empty_base", []),
    ("singleton_base", [7]),
    ("two_ascending_head_false", [1, 2]),
    ("two_descending_head_true", [2, 1]),
    ("tail_drop_recursive_nonminusone", [1, 4, 3]),
    ("multiple_drops_choose_largest", [5, 1, 4, 2, 3]),
    ("negative_distinct", [-1, -5, -3, -9]),
    ("large_integers", [10**100, -(10**120), 7, -(10**140)]),
    ("distinct_floats", [1.25, -4.5, 7.75, 0.0]),
    ("distinct_strings", ["ant", "bee", "yak", "cat"]),
]

rng = random.Random(135)
random_cases = []
for case_number in range(1000):
    length = rng.randrange(0, 61)
    values = rng.sample(range(-5000, 5001), length)
    random_cases.append((f"random_{case_number}", values))

long_cases = [
    ("long_ascending_900", list(range(900))),
    ("long_ascending_1000", list(range(1000))),
    ("long_descending_1200", list(range(1200, 0, -1))),
]

mismatches = []
total = 0


def check(label, value):
    global total
    total += 1
    trusted = outcome(canonical, value)
    candidate = outcome(generated, value)
    if trusted != candidate:
        mismatches.append((label, value, trusted, candidate))


for label, value in documented_and_branch_cases:
    check(label, value)

permutation_count = 0
for length in range(0, 9):
    for permutation in itertools.permutations(range(length)):
        check(f"permutation_n{length}", list(permutation))
        permutation_count += 1

for label, value in random_cases:
    check(label, value)

for label, value in long_cases:
    check(label, value)

print(f"PYTHON_VERSION {sys.version.split()[0]}")
print(f"RECURSION_LIMIT {sys.getrecursionlimit()}")
print(
    "SCOPE "
    f"documented_branch_cases={len(documented_and_branch_cases)} "
    f"exhaustive_distinct_permutations_n0_through_n8={permutation_count} "
    f"seeded_random_distinct_integer_arrays={len(random_cases)} "
    f"long_valid_integer_arrays={len(long_cases)} total={total}"
)
print(f"MISMATCH_COUNT {len(mismatches)}")
for label, value, trusted, candidate in mismatches[:20]:
    print(
        f"MISMATCH label={label} input={describe(value)} "
        f"canonical={trusted!r} generated={candidate!r}"
    )
if len(mismatches) > 20:
    print(f"OMITTED_MISMATCHES {len(mismatches) - 20}")

raise SystemExit(1 if mismatches else 0)
