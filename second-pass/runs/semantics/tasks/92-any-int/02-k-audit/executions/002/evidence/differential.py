#!/usr/bin/env python3
"""Independent differential check: trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random
import sys


SCRATCH = Path("/tmp/audit-work/92-any-int")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", SCRATCH / "canonical.py").any_int
generated = load("submitted_solution", SCRATCH / "solution.py").any_int

named_cases = [
    ("example_xy", (5, 2, 7)),
    ("example_false", (3, 2, 2)),
    ("example_negative", (3, -2, 1)),
    ("example_nonint", (3.6, -2.2, 2)),
    ("xz_branch", (5, 7, 2)),
    ("yz_branch", (7, 5, 2)),
    ("all_zero", (0, 0, 0)),
    ("zero_false", (0, 0, 1)),
    ("negative_xy", (-5, 2, -3)),
    ("negative_xz", (-5, -3, 2)),
    ("negative_yz", (-3, -5, 2)),
    ("nonint_x", (1.0, 2, 3)),
    ("nonint_y", (1, 2.0, 3)),
    ("nonint_z", (1, 2, 3.0)),
    ("large_true", (10**120, -(10**120), 0)),
    ("large_false", (10**120, 10**120, 1)),
    ("bool_true", (True, False, True)),
    ("bool_all_false", (False, False, False)),
]

sample_values = [
    -10,
    -2,
    -1,
    0,
    1,
    2,
    10,
    -2.5,
    -1.0,
    0.0,
    1.0,
    2.5,
    False,
    True,
]
cartesian_cases = list(itertools.product(sample_values, repeat=3))

rng = random.Random(920026)
random_cases: list[tuple[object, object, object]] = []
for _ in range(5000):
    values: list[object] = []
    for _position in range(3):
        kind = rng.randrange(4)
        if kind == 0:
            values.append(rng.randint(-(10**40), 10**40))
        elif kind == 1:
            values.append(rng.randint(-1000, 1000) / 4.0)
        elif kind == 2:
            values.append(bool(rng.getrandbits(1)))
        else:
            values.append(rng.choice((-1, 0, 1, 2, 10**100, -(10**100))))
    random_cases.append(tuple(values))

mismatches: list[tuple[tuple[object, object, object], object, object]] = []

print("NAMED_CASES_BEGIN")
for label, args in named_cases:
    expected = canonical(*args)
    actual = generated(*args)
    print(f"{label}: args={args!r} canonical={expected!r} generated={actual!r}")
    if expected != actual or type(expected) is not type(actual):
        mismatches.append((args, expected, actual))
print("NAMED_CASES_END")

for args in cartesian_cases + random_cases:
    expected = canonical(*args)
    actual = generated(*args)
    if expected != actual or type(expected) is not type(actual):
        mismatches.append((args, expected, actual))

print(f"CARTESIAN_VALUES={sample_values!r}")
print(f"CARTESIAN_CASES={len(cartesian_cases)}")
print("RANDOM_SEED=920026")
print(f"RANDOM_CASES={len(random_cases)}")
print(f"TOTAL_CALLS={len(named_cases) + len(cartesian_cases) + len(random_cases)}")
print(f"MISMATCHES={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

sys.exit(0 if not mismatches else 1)
