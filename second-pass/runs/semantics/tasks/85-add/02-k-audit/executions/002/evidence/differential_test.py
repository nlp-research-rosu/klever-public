#!/usr/bin/env python3
"""Independent differential test for HumanEval/85 add."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random


WORK = Path("/tmp/audit-work/85-add")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


canonical_add = load_function("trusted_canonical_85", WORK / "canonical.py")
generated_add = load_function("candidate_generated_85", WORK / "solution.py")

documented_and_boundaries = [
    [4, 2, 6, 7],
    [],  # outside the non-empty contract, but useful as a robustness boundary
    [0],
    [1],
    [2],
    [-2],
    [1, 0],
    [1, 1],
    [1, 2],
    [1, -2],
    [2, 3, 4],
    [2, 4, 3],
    [-2, -4, -6, -8],
    [0, 0, 0, 0],
    [1, 3, 4, -6, 8, 10],
    [10**100, -(10**100), 2, 10**100 + 1],
    [-(10**100), 10**100, -(10**100), -(10**100)],
]

checks = 0
mismatches: list[tuple[list[int], int, int]] = []


def check(values: list[int]) -> None:
    global checks
    expected = canonical_add(values)
    actual = generated_add(values)
    checks += 1
    if expected != actual:
        mismatches.append((values, expected, actual))


for values in documented_and_boundaries:
    check(values)
    print(
        "explicit "
        f"input={values!r} canonical={canonical_add(values)!r} "
        f"generated={generated_add(values)!r}"
    )

# Exhaust every list through length five over values that straddle parity,
# sign, and zero boundaries.
alphabet = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
for length in range(0, 6):
    for values in product(alphabet, repeat=length):
        check(list(values))

# Deterministic broader representatives, including long lists and large ints.
rng = random.Random(850085)
for _ in range(2500):
    length = rng.randrange(1, 101)
    values = [rng.randrange(-(10**30), 10**30 + 1) for _ in range(length)]
    check(values)

print(f"checks={checks}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"mismatch={mismatch!r}")
    raise SystemExit(1)
print("differential_status=PASS")
