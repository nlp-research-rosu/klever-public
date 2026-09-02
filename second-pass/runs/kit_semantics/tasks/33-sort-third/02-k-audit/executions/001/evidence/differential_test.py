#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/33."""

from __future__ import annotations

import importlib.util
import itertools
import pathlib
import random


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")


def load_function(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_function("generated_solution", SCRATCH / "solution.py")

documented_and_boundaries = [
    [1, 2, 3],
    [5, 6, 3, 4, 8, 9, 2],
    [],
    [1],
    [2, 1],
    [3, 2, 1],
    [9, 8, 7, 6],
    [9, 8, 7, 6, 5],
    [9, 8, 7, 6, 5, 4],
    [9, 8, 7, 6, 5, 4, 3],
    [4, 0, 0, 3, 0, 0, 2, 0, 0, 1],
    [-1, 2, -3, -4, 5, -6, -7],
    [3, 3, 3, 1, 1, 1, 2, 2, 2, 0],
    [True, 8, 7, False, 5, 4, True],
    [3.5, 2.0, -7.5, -2.25, 0.0, 10.5, 1.125],
    list(""),
    list("a"),
    list("sortthird"),
    list("zyxwvutsrqpon"),
]

cases: list[list[object]] = list(documented_and_boundaries)
for length in range(7):
    cases.extend(
        list(values)
        for values in itertools.product(range(-2, 3), repeat=length)
    )
for length in range(6):
    cases.extend(
        list(values)
        for values in itertools.product("abc", repeat=length)
    )

rng = random.Random(330072026)
for _ in range(2_000):
    length = rng.randrange(0, 101)
    cases.append([rng.randint(-10_000, 10_000) for _ in range(length)])

mismatches = []
mutations = []
for index, source in enumerate(cases):
    before = list(source)
    try:
        expected = ("return", canonical(source))
    except Exception as error:  # Included to compare normal/exceptional behavior.
        expected = ("raise", type(error), str(error))
    if source != before:
        mutations.append(("canonical", index, before, source))
    source[:] = before
    try:
        actual = ("return", candidate(source))
    except Exception as error:
        actual = ("raise", type(error), str(error))
    if source != before:
        mutations.append(("candidate", index, before, source))
    if actual != expected:
        mismatches.append((index, before, expected, actual))

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print("exhaustive_integer_lengths=0..6 values=-2..2")
print("exhaustive_string_lengths=0..5 alphabet=abc")
print("random_integer_cases=2000 lengths=0..100 seed=330072026")
print(f"total_cases={len(cases)}")
print(f"input_mutations={len(mutations)}")
print(f"mismatches={len(mismatches)}")
if mutations:
    print(f"first_mutation={mutations[0]!r}")
if mismatches:
    print(f"first_mismatch={mismatches[0]!r}")
raise SystemExit(1 if mutations or mismatches else 0)
