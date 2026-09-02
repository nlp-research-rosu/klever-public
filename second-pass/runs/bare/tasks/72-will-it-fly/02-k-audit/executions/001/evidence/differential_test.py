#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test.

Input scope:
* all four documented examples;
* explicit empty, singleton, balance, and weight-boundary cases;
* every list of length 0..5 over {-2,-1,0,1,2}, with every w in [-8,8];
* 2,500 deterministic random cases of length 0..10.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


scratch = Path(sys.argv[1]).resolve()
canonical = load_entry(scratch / "trusted-canonical.py", "trusted_canonical")
generated = load_entry(scratch / "solution.py", "generated_solution")

documented = [
    ([1, 2], 5, False),
    ([3, 2, 3], 1, False),
    ([3, 2, 3], 9, True),
    ([3], 5, True),
]

explicit = [
    ([], -1),
    ([], 0),
    ([], 1),
    ([0], -1),
    ([0], 0),
    ([1, 2], 2),
    ([1, 2], 3),
    ([3, 2, 3], 7),
    ([3, 2, 3], 8),
    ([-2, 5, -2], 0),
    ([-2, 5, -2], 1),
    ([2, -5, 2], -2),
    ([2, -5, 2], -1),
    ([10**30, 0, 10**30], 2 * 10**30),
    ([-10**30, 1, -10**30], -2 * 10**30),
]

checked = 0
mismatches: list[tuple[list[int], int, object, object]] = []


def check(q: list[int], w: int) -> None:
    global checked
    expected = canonical(q, w)
    actual = generated(q, w)
    checked += 1
    if expected != actual or type(expected) is not bool or type(actual) is not bool:
        mismatches.append((q, w, expected, actual))


for q, w, expected in documented:
    canonical_result = canonical(q, w)
    if canonical_result is not expected:
        raise AssertionError((q, w, expected, canonical_result))
    check(q, w)

for q, w in explicit:
    check(q, w)

alphabet = (-2, -1, 0, 1, 2)
for length in range(6):
    for values in itertools.product(alphabet, repeat=length):
        for w in range(-8, 9):
            check(list(values), w)

rng = random.Random(720072)
for _ in range(2500):
    length = rng.randrange(0, 11)
    q = [rng.randrange(-20, 21) for _ in range(length)]
    w = rng.randrange(-60, 61)
    check(q, w)

print("ORACLE: trusted-canonical.py::will_it_fly")
print("SUBJECT: solution.py::will_it_fly")
print("DOCUMENTED_CASES:", len(documented))
print("EXPLICIT_BOUNDARY_CASES:", len(explicit))
print("EXHAUSTIVE_SCOPE: lengths=0..5 alphabet=-2..2 weights=-8..8")
print("RANDOM_SCOPE: seed=720072 cases=2500 lengths=0..10 values=-20..20 weights=-60..60")
print("TOTAL_CHECKED:", checked)
print("MISMATCHES:", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH:", mismatch)

raise SystemExit(1 if mismatches else 0)
