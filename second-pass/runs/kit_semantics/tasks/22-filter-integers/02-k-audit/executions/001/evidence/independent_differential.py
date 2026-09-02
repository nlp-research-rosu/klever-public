#!/usr/bin/env python3
"""Independent differential check for HumanEval 22.

Run from the scratch reconstruction directory.  `canonical.py` is the trusted
oracle copied from /reference; `solution.py` is the submitted implementation
copied from /candidate.
"""

from __future__ import annotations

import itertools
import random

from canonical import filter_integers as canonical_filter
from solution import filter_integers as submitted_filter


class IntSubclass(int):
    pass


def checked(case: list[object], label: str) -> None:
    expected = canonical_filter(case)
    actual = submitted_filter(case)
    if actual != expected:
        raise AssertionError(
            f"{label}: input={case!r}, canonical={expected!r}, submitted={actual!r}"
        )
    expected_ids = [id(value) for value in expected]
    actual_ids = [id(value) for value in actual]
    if actual_ids != expected_ids:
        raise AssertionError(
            f"{label}: retained objects/order differ: "
            f"canonical_ids={expected_ids!r}, submitted_ids={actual_ids!r}"
        )


documented_and_boundaries = [
    ["a", 3.14, 5],
    [1, 2, 3, "abc", {}, []],
    [],
    [0],
    [-1],
    [True, False],
    [IntSubclass(7), 8.0, IntSubclass(-9)],
    [None, 0, None],
    [0, "", 1],
    ["", 0, 1],
    [0, 1, ""],
    [2**200, -(2**200)],
]

for index, case in enumerate(documented_and_boundaries):
    checked(case, f"boundary-{index}")

pool: tuple[object, ...] = (
    -1,
    0,
    1,
    True,
    False,
    3.14,
    "x",
    None,
    (),
    [],
    {},
    IntSubclass(11),
)

exhaustive_count = 0
for length in range(5):
    for values in itertools.product(pool, repeat=length):
        checked(list(values), f"product-{length}-{exhaustive_count}")
        exhaustive_count += 1

rng = random.Random(220730)
random_count = 2_000
for index in range(random_count):
    length = rng.randrange(0, 41)
    checked(
        [rng.choice(pool) for _ in range(length)],
        f"random-{index}",
    )

print(
    "documented_boundary_cases="
    f"{len(documented_and_boundaries)} "
    f"exhaustive_lists={exhaustive_count} "
    f"random_lists={random_count} mismatches=0"
)
