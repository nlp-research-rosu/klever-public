#!/usr/bin/env python3
"""Independent fidelity tests for HumanEval/43.

Input scope:
* every documented example;
* targeted empty/singleton/zero/duplicate/early/late-pair boundaries;
* every list of length 0..6 over integers -3..3 (137,257 lists);
* 5,000 deterministic pseudorandom lists of length 0..30 over
  [-1_000_000, 1_000_000];
* large Python integers and deliberately placed first/last pairs.

The trusted canonical and submitted generated entry points are imported from
distinct files. A separate direct mathematical oracle is also checked.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random

ROOT = Path("/tmp/audit-work")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "canonical.py").pairs_sum_to_zero
generated = load("submitted_generated", ROOT / "solution.py").pairs_sum_to_zero


def oracle(values: list[int]) -> bool:
    return any(values[i] + values[j] == 0
               for i in range(len(values))
               for j in range(i + 1, len(values)))


targeted = [
    [1, 3, 5, 0],
    [1, 3, -2, 1],
    [1, 2, 3, 7],
    [2, 4, -5, 3, 5, 7],
    [1],
    [],
    [0],
    [0, 0],
    [0, 1],
    [1, 0],
    [1, -1],
    [-1, 1],
    [1, 2, -1],
    [1, 2, -2],
    [5, 5, -5],
    [5, -5, 9, -9],
    [7, 7, 7],
    [-8, 3, 8],
    [10**100, -(10**100)],
    [-(10**200), 3, 10**200],
    [10**100, 1, -(10**100)],
]

checked = 0
category_counts = {"true": 0, "false": 0}


def check(values: list[int], source: str) -> None:
    global checked
    c = canonical(values.copy())
    g = generated(values.copy())
    o = oracle(values)
    if not isinstance(c, bool) or not isinstance(g, bool):
        raise AssertionError(
            f"non-bool result source={source} input={values!r} canonical={c!r} generated={g!r}"
        )
    if c != g or g != o:
        raise AssertionError(
            f"mismatch source={source} input={values!r} canonical={c!r} "
            f"generated={g!r} oracle={o!r}"
        )
    checked += 1
    category_counts["true" if g else "false"] += 1


for case in targeted:
    check(case, "targeted")

alphabet = tuple(range(-3, 4))
exhaustive_count = 0
for length in range(7):
    for values in itertools.product(alphabet, repeat=length):
        check(list(values), "exhaustive")
        exhaustive_count += 1

rng = random.Random(430043)
random_count = 5_000
for _ in range(random_count):
    length = rng.randrange(31)
    values = [rng.randint(-1_000_000, 1_000_000) for _ in range(length)]
    if length >= 2 and rng.randrange(4) == 0:
        i, j = sorted(rng.sample(range(length), 2))
        values[j] = -values[i]
    check(values, "random")

print(f"targeted_cases={len(targeted)}")
print(f"exhaustive_alphabet={alphabet} lengths=0..6 cases={exhaustive_count}")
print(f"random_seed=430043 random_cases={random_count} random_lengths=0..30")
print(f"total_cases={checked} true_results={category_counts['true']} false_results={category_counts['false']}")
print("mismatches=0")
