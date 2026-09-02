#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/142."""

from __future__ import annotations

import importlib.util
import random
import sys


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry(
    "trusted_canonical_142", "/tmp/audit-work/differential/trusted_canonical.py"
)
candidate = load_entry(
    "generated_candidate_142", "/tmp/audit-work/differential/generated_solution.py"
)


def outcome(function, values):
    try:
        return ("return", function(list(values)))
    except Exception as error:
        return ("exception", type(error).__name__, str(error))


cases = [
    ("example-positive", [1, 2, 3]),
    ("example-empty", []),
    ("example-negative", [-1, -5, 2, -1, -5]),
    ("index-0-square", [5]),
    ("index-1-unchanged", [5, -7]),
    ("index-2-unchanged", [5, -7, 11]),
    ("index-3-square", [0, 0, 0, -4]),
    ("index-4-cube", [0, 0, 0, 0, -3]),
    ("index-6-square", [0, 0, 0, 0, 0, 0, -4]),
    ("index-8-cube", [0, 0, 0, 0, 0, 0, 0, 0, -3]),
    ("index-12-square-precedence", [0] * 12 + [-3]),
    ("large-magnitudes", [10**30, -(10**30), 0, -1, 1]),
]

# Deterministically cover every possible final-index branch around 0, 3, 4, 6,
# 8, and the shared 3/4 boundary 12.
for length in range(17):
    cases.append((f"length-boundary-{length}", [i - 8 for i in range(length)]))

# Representative generated inputs, with a fixed seed and documented bounds.
rng = random.Random(142)
for test_no in range(500):
    length = rng.randrange(0, 61)
    values = [rng.randrange(-20, 21) for _ in range(length)]
    cases.append((f"generated-{test_no:03d}", values))

# A real-CPython execution boundary: the candidate is recursively defined while
# the trusted canonical is iterative. These remain valid lists of integers.
for length in (900, 950, 975, 990, 995, 1000, 1001, 1050, 1100):
    cases.append((f"recursion-boundary-{length}", [1] * length))

mismatches = []
for name, values in cases:
    expected = outcome(canonical, values)
    actual = outcome(candidate, values)
    if expected != actual:
        mismatches.append((name, len(values), expected, actual))

print(f"python={sys.version.split()[0]}")
print("oracle=scratch copy of /reference/canonical.py:sum_squares")
print("candidate=scratch copy of /candidate/solution.py:sum_squares")
print("generated_seed=142 generated_cases=500 lengths=[0,60] values=[-20,20]")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
