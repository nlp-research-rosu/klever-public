#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential checks."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derivative


canonical = load_entry(Path("/tmp/audit-work/trusted-62/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/reconstruction-62/solution.py"), "generated_solution"
)


fixed_cases = [
    [],
    [7],
    [0, 9],
    [3, 1, 2, 4, 5],
    [1, 2, 3],
    [0, -2, 3, -4],
    [10**50, -(10**40), 0, 10**30],
    [True, False, True, True],
    [1.5, -2.25, 0.0, 7.125],
]

safe_cases = list(fixed_cases)
small_values = (-2, 0, 3)
for length in range(7):
    safe_cases.extend(map(list, itertools.product(small_values, repeat=length)))

rng = random.Random(6200260726)
for _ in range(1000):
    safe_cases.append(
        [rng.randint(-(10**9), 10**9) for _ in range(rng.randint(0, 80))]
    )

mismatches = []
for index, xs in enumerate(safe_cases):
    expected = canonical(list(xs))
    actual = candidate(list(xs))
    if actual != expected:
        mismatches.append((index, xs, expected, actual))

print(f"safe-domain cases: {len(safe_cases)}")
print(f"safe-domain mismatches: {len(mismatches)}")
for mismatch in mismatches[:10]:
    print("MISMATCH", repr(mismatch))

# The source contract has no length bound. Record concrete CPython behavior
# beyond the recursive implementation's call-stack capacity separately.
long_xs = list(range(1500))
long_canonical = canonical(long_xs)
try:
    long_candidate = candidate(long_xs)
except BaseException as error:
    long_candidate = f"{type(error).__name__}: {error}"
print(f"long-input length: {len(long_xs)}")
print(f"long canonical returned length: {len(long_canonical)}")
print(f"long candidate outcome: {long_candidate}")

if mismatches:
    sys.exit(1)
