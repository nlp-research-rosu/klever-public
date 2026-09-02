#!/usr/bin/env python3
"""Independent candidate-versus-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


canonical = load_entry("trusted_canonical_92", Path("/reference/canonical.py"))
candidate = load_entry(
    "candidate_solution_92", Path("/tmp/audit-work/92-any-int-audit/solution.py")
)


class IntegerSubclass(int):
    pass


def outcome(function, args):
    try:
        value = function(*args)
        return ("return", type(value).__name__, repr(value))
    except BaseException as err:  # Compare observable failure, too.
        return ("raise", type(err).__name__, str(err))


named_cases = [
    ("example-first-sum", (5, 2, 7)),
    ("example-none", (3, 2, 2)),
    ("example-negative", (3, -2, 1)),
    ("example-float", (3.6, -2.2, 2)),
    ("zero-all-branches", (0, 0, 0)),
    ("first-equality-only", (4, 9, 13)),
    ("second-equality-only", (4, 13, 9)),
    ("third-equality-only", (13, 4, 9)),
    ("negative-first-equality", (-7, 3, -4)),
    ("large-first-equality", (10**200, -(10**199), 9 * 10**199)),
    ("bools-true", (True, True, 2)),
    ("bools-false", (True, False, False)),
    ("bool-value-boundary", (False, False, False)),
    ("float-first-short-circuit", (1.0, 1, 2)),
    ("float-second-short-circuit", (1, 1.0, 2)),
    ("float-third-short-circuit", (1, 2, 3.0)),
    ("negative-zero-float", (-0.0, 0, 0)),
    ("nan", (math.nan, 0, 0)),
    ("positive-infinity", (math.inf, 0, 0)),
    ("complex-number", (1 + 0j, 1, 2)),
    ("decimal-number", (Decimal("1"), 1, 2)),
    ("fraction-number", (Fraction(1, 1), 1, 2)),
    ("integer-subclass", (IntegerSubclass(1), IntegerSubclass(2), IntegerSubclass(3))),
    ("empty-invalid-value", ([], 1, 1)),
    ("none-invalid-value", (None, 1, 1)),
]

mismatches = []
total = 0
for label, args in named_cases:
    expected = outcome(canonical, args)
    actual = outcome(candidate, args)
    total += 1
    print(f"NAMED {label}: args={args!r} canonical={expected} candidate={actual}")
    if expected != actual:
        mismatches.append((label, args, expected, actual))

# Exhaust the primitive branch/type grid. This covers each position with all
# small Int and Bool values and several Float boundary values.
grid_values = [
    -3,
    -2,
    -1,
    0,
    1,
    2,
    3,
    False,
    True,
    -0.0,
    0.5,
    -2.25,
    math.inf,
    -math.inf,
    math.nan,
]
for args in itertools.product(grid_values, repeat=3):
    expected = outcome(canonical, args)
    actual = outcome(candidate, args)
    total += 1
    if expected != actual:
        mismatches.append(("grid", args, expected, actual))

# Representative unbounded integer sampling, with deliberately planted true
# cases in all three equality positions and neighboring false cases.
rng = random.Random(9200729)
for index in range(5000):
    width = rng.choice([1, 8, 31, 63, 127, 257, 1024])
    x = rng.randrange(-(1 << width), 1 << width)
    y = rng.randrange(-(1 << width), 1 << width)
    branch = index % 4
    if branch == 0:
        args = (x, y, x + y)
    elif branch == 1:
        args = (x, x + y, y)
    elif branch == 2:
        args = (x + y, x, y)
    else:
        args = (x, y, x + y + 1)
    expected = outcome(canonical, args)
    actual = outcome(candidate, args)
    total += 1
    if expected != actual:
        mismatches.append(("random-int", args, expected, actual))

# CPython call-boundary behavior for missing/excess arguments.
for label, args in [
    ("no-arguments", ()),
    ("one-argument", (1,)),
    ("two-arguments", (1, 2)),
    ("four-arguments", (1, 2, 3, 4)),
]:
    expected = outcome(canonical, args)
    actual = outcome(candidate, args)
    total += 1
    print(f"CALL {label}: canonical={expected} candidate={actual}")
    if expected != actual:
        mismatches.append((label, args, expected, actual))

print(f"SUMMARY total={total} mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
