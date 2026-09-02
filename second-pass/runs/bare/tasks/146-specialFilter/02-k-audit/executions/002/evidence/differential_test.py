#!/usr/bin/env python3
"""Differential checks between the trusted canonical and submitted solution."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated = load_module(
    "submitted_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)


def result_for(function, values: list[int]) -> int:
    return function(list(values))


def check(values: list[int], label: str) -> None:
    global checks
    expected = result_for(canonical.specialFilter, values)
    actual = result_for(generated.specialFilter, values)
    checks += 1
    if type(actual) is not type(expected) or actual != expected:
        mismatches.append((label, values, expected, actual))


checks = 0
mismatches: list[tuple[str, list[int], object, object]] = []

# Documented examples, emptiness, strict >10 threshold, and repeat counting.
fixed_cases = [
    ("prompt-example-1", [15, -73, 14, -15]),
    ("prompt-example-2", [33, -2, -3, 45, 21, 109]),
    ("empty", []),
    ("strict-threshold", [-999, -11, 0, 1, 9, 10, 11]),
    ("repeat-count", [15, 15, 15, 20, 20]),
    ("all-branches", [11, 12, 21, 22, 313, 314, 423, 424]),
]
for case_label, case_values in fixed_cases:
    check(case_values, case_label)

# Exhaust all singleton integers through several digit-width transitions.
for value in range(-250, 2001):
    check([value], f"singleton-{value}")

# Exercise arbitrary-precision boundaries not present in the submitted spec.
wide_values = [
    10,
    11,
    12,
    19,
    20,
    21,
    29,
    31,
    39,
    91,
    99,
    100,
    101,
    109,
    111,
    199,
    909,
    999,
    1000,
    1001,
    1009,
    1011,
    3003,
    70000000000000000000000000000000000000000000000009,
    80000000000000000000000000000000000000000000000007,
    90000000000000000000000000000000000000000000000009,
]
for value in wide_values:
    check([value], f"wide-singleton-{value}")
check(wide_values, "wide-combined")

# Exhaust representative two-element interactions to detect state leakage.
pair_values = [-73, 0, 9, 10, 11, 12, 15, 20, 21, 33, 45, 99, 100, 101, 109, 313, 999, 1001]
for left in pair_values:
    for right in pair_values:
        check([left, right], f"pair-{left}-{right}")

# Deterministic generated arrays, including very large positive/negative ints.
rng = random.Random(146)
pool = list(range(-30, 151)) + wide_values
for index in range(1500):
    length = rng.randrange(0, 25)
    values = [rng.choice(pool) for _ in range(length)]
    if index % 10 == 0:
        magnitude = rng.randrange(1, 10**40)
        values.append(magnitude if index % 20 == 0 else -magnitude)
    check(values, f"generated-{index}")

print(f"checks={checks}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))
raise SystemExit(1 if mismatches else 0)
