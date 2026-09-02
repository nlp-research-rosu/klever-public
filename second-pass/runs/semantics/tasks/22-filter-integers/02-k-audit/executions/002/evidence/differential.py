#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted Python."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


class IntSubclass(int):
    pass


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


canonical = load_function("trusted_canonical", "/reference/canonical.py")
generated = load_function(
    "submitted_solution", "/tmp/audit-work/22-filter-integers/solution.py"
)

documented_and_boundaries = [
    ["a", 3.14, 5],
    [1, 2, 3, "abc", {}, []],
    [],
    [0],
    [-1],
    [True, False],
    [IntSubclass(7), IntSubclass(-2)],
    [-(2**200), 2**200],
    [0.0, -0.0, float("inf"), float("-inf")],
    [None, "", (), {}, [], set()],
    ["left", 1, False, 2.5, -3, [], 4, "right"],
]

atom_pool = [
    -1,
    0,
    2**80,
    False,
    True,
    2.5,
    "",
    "x",
    None,
    (),
    IntSubclass(9),
]

cases = list(documented_and_boundaries)
for length in range(5):
    cases.extend(list(items) for items in itertools.product(atom_pool, repeat=length))

mismatches = []
for index, values in enumerate(cases):
    expected = canonical(values)
    actual = generated(values)
    if actual != expected or [type(x) for x in actual] != [type(x) for x in expected]:
        mismatches.append((index, repr(values), repr(expected), repr(actual)))

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print(f"exhaustive_generated_cases={sum(len(atom_pool) ** n for n in range(5))}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)
assert not mismatches
print("differential=PASS")
