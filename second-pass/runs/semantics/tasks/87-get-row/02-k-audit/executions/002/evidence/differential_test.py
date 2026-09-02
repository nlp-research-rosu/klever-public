#!/usr/bin/env python3
"""Independent differential test for HumanEval/87 over integer ragged lists."""

from __future__ import annotations

from itertools import product
import importlib.util
from pathlib import Path
import random


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("/reference/canonical.py", "trusted_canonical").get_row
generated = load("/candidate/solution.py", "candidate_solution").get_row


DOCUMENTED = [
    (
        [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 1, 6],
            [1, 2, 3, 4, 5, 1],
        ],
        1,
    ),
    ([], 1),
    ([[], [1], [1, 2, 3]], 3),
]

BOUNDARY = [
    ([[]], 0),
    ([[], [], []], -1),
    ([[0]], 0),
    ([[0]], 1),
    ([[-1, -1, 0, -1]], -1),
    ([[2, 1, 2], [], [2], [0, 2, 2, 2]], 2),
    ([[10**50, -(10**50)]], 10**50),
]


def check_case(lst: list[list[int]], x: int, label: str) -> None:
    expected = canonical(lst, x)
    actual = generated(lst, x)
    if actual != expected:
        raise AssertionError(
            f"{label}: lst={lst!r} x={x!r} canonical={expected!r} generated={actual!r}"
        )


def main() -> None:
    total = 0
    for i, (lst, x) in enumerate(DOCUMENTED):
        check_case(lst, x, f"documented-{i}")
        total += 1
    for i, (lst, x) in enumerate(BOUNDARY):
        check_case(lst, x, f"boundary-{i}")
        total += 1

    values = (-1, 0, 1)
    row_variants: list[list[int]] = [[]]
    for length in (1, 2):
        row_variants.extend([list(items) for items in product(values, repeat=length)])
    exhaustive = 0
    for outer_length in range(4):
        for rows in product(row_variants, repeat=outer_length):
            lst = [list(row) for row in rows]
            for x in values:
                check_case(lst, x, "exhaustive-small")
                total += 1
                exhaustive += 1

    rng = random.Random(870087)
    random_cases = 2000
    for _ in range(random_cases):
        lst = [
            [rng.randint(-100, 100) for _ in range(rng.randint(0, 12))]
            for _ in range(rng.randint(0, 9))
        ]
        x = rng.randint(-105, 105)
        check_case(lst, x, "deterministic-random")
        total += 1

    print(f"documented_cases={len(DOCUMENTED)}")
    print(f"boundary_cases={len(BOUNDARY)}")
    print(f"exhaustive_small_cases={exhaustive}")
    print(f"deterministic_random_cases={random_cases}")
    print(f"total_cases={total}")
    print("mismatches=0")


if __name__ == "__main__":
    main()
