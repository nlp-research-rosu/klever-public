#!/usr/bin/env python3
"""Generate deterministic K ground claims comparing nsScan to canonical.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_canonical():
    path = Path("/reference/canonical.py")
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_k", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


def ints_term(values: list[int]) -> str:
    term = "nilInts"
    for value in reversed(values):
        term = f"consInts({value}, {term})"
    return term


canonical = load_canonical()
cases = [
    [],
    [1],
    [1, 1],
    [1, 2],
    [2, 1],
    [3, 1, 2, 1],
    [0, -1, 0],
    [10**80, 10**79, 10**81],
    [-(10**80), -(10**79), -(10**81)],
]
for length in range(4):
    cases.extend([list(values) for values in itertools.product(range(-2, 3), repeat=length)])
rng = random.Random(900090)
for _ in range(200):
    cases.append([rng.randrange(-20, 21) for _ in range(rng.randrange(0, 11))])

unique_cases: list[list[int]] = []
seen: set[tuple[int, ...]] = set()
for case in cases:
    key = tuple(case)
    if key not in seen:
        seen.add(key)
        unique_cases.append(case)

print('requires "verification.k"')
print()
print("module NSSCAN-DIFFERENTIAL-SPEC")
print("  imports NEXT-SMALLEST-VERIFICATION")
print(f"  // Ground inputs checked against trusted canonical.py: {len(unique_cases)}")
for index, values in enumerate(unique_cases):
    expected = canonical(list(values))
    rhs = "noneV" if expected is None else str(expected)
    print(f"  // case {index}: {values!r}")
    print(f"  claim <k> nsScan({ints_term(values)}, 0, 0, 0) => {rhs} </k>")
print("endmodule")
