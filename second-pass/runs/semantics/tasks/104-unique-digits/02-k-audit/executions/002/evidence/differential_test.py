#!/usr/bin/env python3
"""Independent differential test for HumanEval 104.

Oracle: /reference/canonical.py, loaded directly from the trusted mount.
Candidate: /tmp/audit-work/workspace/solution.py, copied from the submission.

Input scope:
* both documented examples;
* empty, singleton, duplicate, already-sorted, and reverse-sorted lists;
* digit-scanner branch boundaries (one digit, trailing even digit, internal
  even digit after an odd suffix, zero digit, all-odd multi-digit values);
* one very large positive Python integer;
* every singleton [n] for 1 <= n <= 9999;
* 2,000 deterministic random lists of length 0..30, with positive elements
  drawn from 1..10**30.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(
    Path("/tmp/audit-work/workspace/solution.py"), "submitted_solution"
)

named_cases = {
    "example_1": [15, 33, 1422, 1],
    "example_2": [152, 323, 1422, 10],
    "empty": [],
    "one_odd_digit": [1],
    "one_even_digit": [2],
    "all_odd_multidigit": [11, 97531, 999999999999999999999999999999],
    "trailing_even_digit": [12, 13572],
    "internal_even_after_odd_suffix": [21, 23451],
    "contains_zero": [101, 13501, 10],
    "duplicates": [33, 11, 33, 11, 33],
    "reverse_order": [999, 777, 555, 333, 111],
    "mixed_boundaries": [1, 2, 9, 10, 11, 12, 19, 20, 21, 22],
}

mismatches = []
executed = 0

for name, values in named_cases.items():
    expected = canonical(list(values))
    actual = candidate(list(values))
    executed += 1
    print(f"NAMED {name}: input={values} canonical={expected} candidate={actual}")
    if expected != actual:
        mismatches.append((name, values, expected, actual))

for number in range(1, 10_000):
    values = [number]
    expected = canonical(values)
    actual = candidate(values)
    executed += 1
    if expected != actual:
        mismatches.append(("exhaustive_singleton", values, expected, actual))

rng = random.Random(104_20260726)
for index in range(2_000):
    values = [rng.randint(1, 10**30) for _ in range(rng.randint(0, 30))]
    expected = canonical(values)
    actual = candidate(values)
    executed += 1
    if expected != actual:
        mismatches.append((f"random_{index}", values, expected, actual))

print(f"TOTAL_CASES: {executed}")
print(f"MISMATCHES: {len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH: {mismatch}")

raise SystemExit(1 if mismatches else 0)
