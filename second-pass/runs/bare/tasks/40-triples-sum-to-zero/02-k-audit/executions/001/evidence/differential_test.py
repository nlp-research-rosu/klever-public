#!/usr/bin/env python3
"""Independent differential test for HumanEval/40.

Oracle: the trusted /reference/canonical.py implementation.
Subject: the scratch-copied candidate solution.py implementation.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triples_sum_to_zero


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "scratch_candidate", Path("/tmp/audit-work/candidate-src/solution.py")
)

documented = [
    ([1, 3, 5, 0], False),
    ([1, 3, -2, 1], True),
    ([1, 2, 3, 7], False),
    ([2, 4, -5, 3, 9, 7], True),
    ([1], False),
]

boundaries = [
    ([], False, "empty entry branch"),
    ([0], False, "one element"),
    ([0, 0], False, "two equal elements are not three positions"),
    ([0, 0, 0], True, "three equal values at distinct positions"),
    ([-1, 0, 1], True, "exactly three, first helper check succeeds"),
    ([1, 1, -2], True, "duplicate values at distinct positions"),
    ([1, -1], False, "values cannot be reused"),
    ([5, 1, 7, -8], True, "match after helper recursion"),
    ([9, 8, 1, 2, -3], True, "match after entry recursion"),
    ([10**30, -(10**30), 0], True, "unbounded integer magnitude"),
    ([10**30, 10**30, -(2 * 10**30)], True, "large arithmetic"),
    ([-7, -6, -5, -4], False, "all negative"),
    ([4, 5, 6, 7], False, "all positive"),
]


def check(values: list[int], expected: bool | None = None) -> None:
    global checked, mismatches
    oracle = canonical(values)
    actual = candidate(values)
    checked += 1
    if expected is not None and oracle is not expected:
        raise AssertionError(
            f"trusted oracle disagrees with stated expected value: {values!r} "
            f"expected={expected!r} oracle={oracle!r}"
        )
    if type(actual) is not bool or actual != oracle:
        mismatches.append((values, oracle, actual))


checked = 0
mismatches: list[tuple[list[int], bool, object]] = []

for values, expected in documented:
    check(values, expected)

for values, expected, _label in boundaries:
    check(values, expected)

# Exhaust every list of lengths 0..6 over a symmetric seven-value alphabet.
alphabet = range(-3, 4)
exhaustive_count = 0
for length in range(7):
    for values in itertools.product(alphabet, repeat=length):
        check(list(values))
        exhaustive_count += 1

# Deterministic representative sampling reaches longer recursive paths and
# values outside the exhaustive alphabet. Half the cases have a forced triple.
rng = random.Random(40040)
generated_count = 1000
for index in range(generated_count):
    length = rng.randrange(0, 31)
    values = [rng.randrange(-100, 101) for _ in range(length)]
    if index % 2 == 0 and length >= 3:
        i, j, k = sorted(rng.sample(range(length), 3))
        values[k] = -values[i] - values[j]
    check(values)

print(f"documented={len(documented)}")
print(f"boundary={len(boundaries)}")
print(
    "exhaustive="
    f"{exhaustive_count} "
    "scope=all lengths 0..6 over integers -3..3"
)
print(
    "generated="
    f"{generated_count} "
    "seed=40040 lengths=0..30 values=-100..100 forced_triple_every_other"
)
print(f"total={checked}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1)
