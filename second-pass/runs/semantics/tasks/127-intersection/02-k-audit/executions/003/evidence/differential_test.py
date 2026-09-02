#!/usr/bin/env python3
"""Independent candidate/canonical/oracle differential test.

The oracle uses a square-root primality test, unlike both submitted programs'
linear divisor search.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independently_prime(number: int) -> bool:
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    return all(number % divisor for divisor in range(3, math.isqrt(number) + 1, 2))


def oracle(interval1: tuple[int, int], interval2: tuple[int, int]) -> str:
    overlap = min(interval1[1], interval2[1]) - max(interval1[0], interval2[0])
    return "YES" if independently_prime(overlap) else "NO"


def main() -> None:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_module(
        "submitted_solution", Path("/candidate/solution.py")
    )

    named_cases = [
        ("prompt example: touching", (1, 2), (2, 3)),
        ("prompt example: length one", (-1, 1), (0, 4)),
        ("prompt example: length two", (-3, -1), (-5, 5)),
        ("canonical-doc example: length five", (-3, 9), (-1, 4)),
        ("disjoint left", (0, 3), (10, 12)),
        ("disjoint right", (10, 12), (0, 3)),
        ("equal singleton", (4, 4), (4, 4)),
        ("distinct singletons", (-1, -1), (1, 1)),
        ("overlap length zero", (0, 5), (5, 9)),
        ("overlap length one", (0, 5), (4, 9)),
        ("overlap length two", (0, 5), (3, 9)),
        ("overlap length three", (0, 5), (2, 9)),
        ("even composite length four", (0, 4), (0, 4)),
        ("odd composite length nine", (-20, -11), (-30, 0)),
        ("prime length ninety-seven", (0, 97), (-4, 110)),
        ("composite length one hundred", (0, 100), (-4, 110)),
        ("left selected from interval1", (3, 20), (0, 15)),
        ("left selected from interval2", (0, 15), (3, 20)),
        ("right selected from interval1", (0, 15), (3, 20)),
        ("right selected from interval2", (3, 20), (0, 15)),
        ("identical negative interval", (-100, -89), (-100, -89)),
        (
            "large positive translation",
            (10**30, 10**30 + 101),
            (10**30, 10**30 + 101),
        ),
        (
            "large negative translation",
            (-10**30 - 49, -10**30),
            (-10**30 - 49, -10**30),
        ),
    ]

    checked = 0
    mismatches: list[tuple[object, ...]] = []

    def check(label: str, one: tuple[int, int], two: tuple[int, int]) -> None:
        nonlocal checked
        expected = oracle(one, two)
        canonical_result = canonical.intersection(one, two)
        candidate_result = candidate.intersection(one, two)
        checked += 1
        if not (expected == canonical_result == candidate_result):
            mismatches.append(
                (label, one, two, expected, canonical_result, candidate_result)
            )

    for label, one, two in named_cases:
        check(label, one, two)

    # Exhaust every pair of valid closed intervals with endpoints in [-8, 8].
    intervals = [(a, b) for a in range(-8, 9) for b in range(a, 9)]
    for one in intervals:
        for two in intervals:
            check("exhaustive endpoints [-8,8]", one, two)

    # Deterministic broader cases span negative/positive coordinates and lengths.
    generator = random.Random(127)
    for _ in range(5000):
        a = generator.randint(-10**6, 10**6)
        b = a + generator.randint(0, 500)
        c = generator.randint(-10**6, 10**6)
        d = c + generator.randint(0, 500)
        check("deterministic generated", (a, b), (c, d))

    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_intervals={len(intervals)}")
    print(f"generated_cases=5000")
    print(f"total_cases={checked}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print("MISMATCH", mismatch)
        raise AssertionError("differential mismatch")
    print("DIFFERENTIAL_PASS")


if __name__ == "__main__":
    main()
