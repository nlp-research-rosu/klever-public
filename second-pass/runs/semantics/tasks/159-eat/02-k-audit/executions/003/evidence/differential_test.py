#!/usr/bin/env python3
"""Independent differential test for HumanEval/159.

The oracle and candidate are imported from paths supplied on the command line.
The test exhausts every (need, remaining) pair for four representative number
values, then adds deterministic random coverage across the complete contract
cube.  It also checks all documented examples and explicit branch boundaries.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(oracle, candidate, case: tuple[int, int, int]) -> None:
    expected = oracle.eat(*case)
    actual = candidate.eat(*case)
    if actual != expected:
        raise AssertionError(
            f"mismatch input={case}: canonical={expected!r}, candidate={actual!r}"
        )


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} CANONICAL.py SOLUTION.py")
        return 2

    oracle = load(sys.argv[1], "trusted_canonical")
    candidate = load(sys.argv[2], "generated_solution")

    examples = [
        (5, 6, 10),
        (4, 8, 9),
        (1, 10, 10),
        (2, 11, 5),
    ]
    boundaries = [
        (0, 0, 0),
        (1000, 0, 0),
        (0, 1000, 1000),
        (1000, 1000, 1000),
        (0, 1, 0),
        (1000, 1, 0),
        (0, 999, 1000),
        (1000, 1000, 999),
        (37, 500, 499),
        (37, 500, 500),
        (37, 500, 501),
    ]

    checked = 0
    for case in examples + boundaries:
        check(oracle, candidate, case)
        checked += 1

    # Exhaust all branch comparisons and arithmetic boundaries for four
    # representative values of the independent additive parameter.
    for number in (0, 1, 999, 1000):
        for need in range(1001):
            for remaining in range(1001):
                check(oracle, candidate, (number, need, remaining))
                checked += 1

    rng = random.Random(159)
    random_count = 100_000
    for _ in range(random_count):
        case = tuple(rng.randrange(1001) for _ in range(3))
        check(oracle, candidate, case)
        checked += 1

    print("documented_examples=4")
    print("explicit_boundary_cases=11")
    print("exhaustive_pair_grid=4*1001*1001")
    print(f"deterministic_random_cases={random_count} seed=159")
    print(f"total_comparisons={checked}")
    print("mismatches=0")
    print("empty_case=not_applicable (the source contract takes three integers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
