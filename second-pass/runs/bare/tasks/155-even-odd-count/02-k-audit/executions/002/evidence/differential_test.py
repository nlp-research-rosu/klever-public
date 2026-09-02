#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "candidate_solution",
    Path("/tmp/audit-work/155-even-odd-count-audit/source/solution.py"),
)

# Explicit examples and branch/boundary cases, followed by an exhaustive
# interval and a deterministic broader arbitrary-precision sample.
explicit = [
    -12,
    123,
    0,
    -1,
    1,
    -2,
    2,
    -9,
    9,
    -10,
    10,
    -11,
    11,
    -19,
    19,
    -20,
    20,
    -99,
    99,
    -100,
    100,
    -101,
    101,
    -9090,
    9090,
    -(10**100),
    10**100,
    -(10**100 + 246813579),
    10**100 + 246813579,
]
rng = random.Random(155)
random_cases = [rng.randint(-(10**200), 10**200) for _ in range(2000)]
cases = list(dict.fromkeys(explicit + list(range(-10000, 10001)) + random_cases))

print("oracle=/reference/canonical.py:even_odd_count")
print(
    "candidate=/tmp/audit-work/155-even-odd-count-audit/source/"
    "solution.py:even_odd_count"
)
print(
    "scope=explicit prompt examples and branch boundaries; every integer "
    "[-10000,10000]; 2000 seed-155 integers in [-10**200,10**200]"
)
print(f"case_count={len(cases)}")

mismatches: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
for value in cases:
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append((value, expected, actual))

print(f"mismatch_count={len(mismatches)}")
for value, expected, actual in mismatches:
    print(f"mismatch input={value} canonical={expected} candidate={actual}")

if mismatches:
    raise SystemExit(1)
