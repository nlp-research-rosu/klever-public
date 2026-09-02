#!/usr/bin/env python3
"""Independent differential test: trusted canonical.py versus candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function("candidate_solution", Path("/candidate/solution.py"))

named_cases = [
    ("documented increasing", [1, 2, 4, 20]),
    ("documented non-monotonic", [1, 20, 4, 10]),
    ("documented decreasing", [4, 1, 0, -10]),
    ("empty", []),
    ("singleton", [0]),
    ("two increasing", [-1, 1]),
    ("two equal", [1, 1]),
    ("two decreasing", [1, -1]),
    ("strictly increasing", [-3, -1, 0, 4]),
    ("nondecreasing with duplicates", [-3, -3, 0, 4, 4]),
    ("strictly decreasing", [4, 0, -1, -3]),
    ("nonincreasing with duplicates", [4, 4, 0, -3, -3]),
    ("all equal", [7, 7, 7, 7]),
    ("up then down", [0, 2, 1]),
    ("down then up", [2, 0, 1]),
    ("late increase after decrease", [5, 4, 3, 4]),
    ("late decrease after increase", [1, 2, 3, 2]),
    ("large magnitudes", [-(10**100), 0, 10**100]),
    ("float increasing", [-1.5, 0.0, 2.75]),
    ("string increasing", ["a", "aa", "b"]),
    ("string decreasing", ["z", "m", "a"]),
    ("booleans", [False, False, True]),
    ("unorderable mixed values", [1, "a"]),
]


def outcome(function, value):
    try:
        return ("return", function(value))
    except Exception as error:  # The exception class is observable behavior here.
        return ("raise", type(error).__name__)


checked = 0
mismatches = []
branch_counts = {"nondecreasing": 0, "nonincreasing_only": 0, "neither": 0}


def compare(label, value):
    global checked
    expected = outcome(canonical, list(value))
    actual = outcome(candidate, list(value))
    checked += 1
    if expected != actual:
        mismatches.append((label, list(value), expected, actual))
    try:
        if all(a <= b for a, b in zip(value, value[1:])):
            branch_counts["nondecreasing"] += 1
        elif all(a >= b for a, b in zip(value, value[1:])):
            branch_counts["nonincreasing_only"] += 1
        else:
            branch_counts["neither"] += 1
    except TypeError:
        pass


for label, value in named_cases:
    compare(label, value)

# Exhaustive small integer domain. This spans all lengths 0..7 over five values.
for length in range(8):
    for value in itertools.product(range(-2, 3), repeat=length):
        compare(f"exhaustive-int-len-{length}", value)

# Deterministic broader generated integer sample.
rng = random.Random(570057)
for index in range(5000):
    length = rng.randrange(0, 31)
    value = [rng.randrange(-10**6, 10**6 + 1) for _ in range(length)]
    compare(f"random-int-{index}", value)

print(f"named_cases={len(named_cases)}")
print("exhaustive_domain=integer lists, lengths 0..7, values -2..2")
print("random_domain=5000 integer lists, lengths 0..30, seed 570057")
print(f"checked={checked}")
print(f"branch_counts={branch_counts}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")
assert not mismatches
print("DIFFERENTIAL_TEST=PASS")
