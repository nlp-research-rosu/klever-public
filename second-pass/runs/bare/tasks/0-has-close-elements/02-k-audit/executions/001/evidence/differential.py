#!/usr/bin/env python3
"""Independent differential check against the trusted HumanEval entry point."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry("submitted_solution", Path("/tmp/audit-work/source/solution.py"))

documented_and_boundaries = [
    ("example_false", [1.0, 2.0, 3.0], 0.5),
    ("example_true", [1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
    ("empty", [], 1.0),
    ("singleton", [1.0], 1.0),
    ("strict_equal_boundary", [1.0, 1.5], 0.5),
    ("strict_just_above", [1.0, 1.5], 0.5000000000000001),
    ("strict_just_below", [1.0, 1.5], 0.49999999999999994),
    ("duplicate_zero_threshold", [2.0, 2.0], 0.0),
    ("duplicate_positive_threshold", [2.0, 2.0], 1e-300),
    ("negative_threshold", [-3.0, -3.0], -1.0),
    ("zero_threshold", [-0.0, 0.0], 0.0),
    ("negative_values", [-10.0, -9.75, 100.0], 0.3),
    ("pair_only_at_end", [100.0, -100.0, 5.0, 5.25], 0.3),
    ("nan_element", [math.nan, 0.0, 0.1], 0.2),
    ("positive_infinity", [math.inf, 0.0, 1.0], 2.0),
    ("infinite_threshold", [0.0, 1.0], math.inf),
]

normal_result_mismatches = []
exceptional_outcome_mismatches = []
checked = 0


def capture(fn, numbers, threshold):
    try:
        return ("return", fn(numbers, threshold))
    except Exception as exc:  # evidence must record host-language divergence
        return ("exception", type(exc).__name__)


def compare(label, numbers, threshold):
    global checked
    checked += 1
    expected = capture(canonical, numbers, threshold)
    actual = capture(candidate, numbers, threshold)
    if expected != actual:
        if len(numbers) <= 20:
            rendered_numbers = repr(numbers)
        else:
            rendered_numbers = (
                f"len={len(numbers)}, head={numbers[:5]!r}, tail={numbers[-5:]!r}"
            )
        record = (label, rendered_numbers, repr(threshold), expected, actual)
        if expected[0] == actual[0] == "return":
            normal_result_mismatches.append(record)
        else:
            exceptional_outcome_mismatches.append(record)


for case in documented_and_boundaries:
    compare(*case)

# Exhaust all short lists over values chosen to exercise equality, signs,
# duplicates, exact threshold boundaries, and both recursive branches.
small_values = (-2.0, -1.0, 0.0, 0.5, 1.0, 2.0)
small_thresholds = (-1.0, 0.0, 0.5, 1.0, 2.0)
for length in range(6):
    for numbers in itertools.product(small_values, repeat=length):
        for threshold in small_thresholds:
            compare("exhaustive_small", list(numbers), threshold)

# Deterministic broader finite-float sample.
rng = random.Random(20260723)
for index in range(2000):
    length = rng.randrange(0, 15)
    numbers = [rng.randint(-1000, 1000) / rng.choice((1, 2, 4, 10, 100))
               for _ in range(length)]
    threshold = rng.randint(-200, 500) / rng.choice((1, 2, 10, 100))
    compare(f"generated_{index}", numbers, threshold)

# The source rewrite uses Python recursion whereas the trusted implementation
# uses loops. This satisfying typed input exposes their CPython termination
# behavior without claiming a normal-return value mismatch.
compare("recursion_depth_boundary", [float(i) for i in range(1100)], -1.0)

print(f"checked_cases={checked}")
print(f"normal_result_mismatches={len(normal_result_mismatches)}")
for mismatch in normal_result_mismatches[:10]:
    print(f"NORMAL_RESULT_MISMATCH {mismatch!r}")
print(f"exceptional_outcome_mismatches={len(exceptional_outcome_mismatches)}")
for mismatch in exceptional_outcome_mismatches[:10]:
    print(f"EXCEPTIONAL_OUTCOME_MISMATCH {mismatch!r}")

sys.exit(1 if normal_result_mismatches else 0)
