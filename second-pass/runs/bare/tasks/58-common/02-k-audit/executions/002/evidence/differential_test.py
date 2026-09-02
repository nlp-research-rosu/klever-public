#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/58."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/58-common-audit")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load_entry(ROOT / "trusted" / "canonical.py", "trusted_canonical")
candidate = load_entry(ROOT / "candidate" / "solution.py", "generated_solution")


def typed_value(value):
    if isinstance(value, list):
        return ("list", tuple(typed_value(item) for item in value))
    if isinstance(value, tuple):
        return ("tuple", tuple(typed_value(item) for item in value))
    return (type(value).__module__, type(value).__qualname__, repr(value))


def outcome(function, left, right):
    try:
        value = function(left, right)
        return ("value", typed_value(value))
    except Exception as error:  # compare specified behavior and exception behavior
        return ("exception", type(error).__name__, str(error))


fixed_cases = [
    ("prompt-example-1", [1, 4, 3, 34, 653, 2, 5], [5, 7, 1, 5, 9, 653, 121]),
    ("prompt-example-2", [5, 3, 2, 8], [3, 2]),
    ("both-empty", [], []),
    ("left-empty", [], [1, 1]),
    ("right-empty", [1, 1], []),
    ("singleton-hit", [0], [0]),
    ("singleton-miss", [0], [1]),
    ("duplicates-and-negatives", [3, 3, -1, 2], [3, -1, -1]),
    ("opposite-order", [5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ("large-integers", [-(10**100), 0, 10**100], [10**100, -(10**100)]),
    ("bool-int-equality", [False, True, 2], [0, 1, 3]),
    ("strings", ["beta", "alpha", "beta"], ["gamma", "alpha"]),
    ("tuples", [(2, 0), (1, 9)], [(1, 9), (3, 0)]),
    ("unhashable-left-no-common", [[1]], []),
    ("unhashable-right-no-common", [], [[1]]),
]

mismatches = []
fixed_mismatches = []
for label, left, right in fixed_cases:
    expected = outcome(canonical, left, right)
    actual = outcome(candidate, left, right)
    print(f"FIXED {label}: left={left!r} right={right!r}")
    print(f"  canonical={expected!r}")
    print(f"  candidate={actual!r}")
    if expected != actual:
        mismatch = (label, left, right, expected, actual)
        mismatches.append(mismatch)
        fixed_mismatches.append(mismatch)

# Exhaust every pair of lists of length 0..3 over {-2,-1,0,1,2}.
small_lists = [
    list(values)
    for length in range(4)
    for values in itertools.product(range(-2, 3), repeat=length)
]
exhaustive_pairs = 0
for left in small_lists:
    for right in small_lists:
        exhaustive_pairs += 1
        expected = outcome(canonical, left, right)
        actual = outcome(candidate, left, right)
        if expected != actual:
            mismatches.append(("exhaustive-int", left, right, expected, actual))

# A fixed seed makes the broader generated sample exactly reproducible.
rng = random.Random(580058)
random_pairs = 2000
for index in range(random_pairs):
    left = [rng.randint(-10**9, 10**9) for _ in range(rng.randint(0, 20))]
    right = [rng.randint(-10**9, 10**9) for _ in range(rng.randint(0, 20))]
    expected = outcome(canonical, left, right)
    actual = outcome(candidate, left, right)
    if expected != actual:
        mismatches.append((f"random-int-{index}", left, right, expected, actual))

print(f"EXHAUSTIVE_INTEGER_PAIRS={exhaustive_pairs}")
print(f"RANDOM_INTEGER_PAIRS={random_pairs} seed=580058")
print(f"FIXED_CASES={len(fixed_cases)}")
print(f"FIXED_MISMATCHES={len(fixed_mismatches)}")
print(f"INTEGER_GENERATED_MISMATCHES={len(mismatches) - len(fixed_mismatches)}")
print(f"MISMATCHES={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    raise SystemExit(1)
