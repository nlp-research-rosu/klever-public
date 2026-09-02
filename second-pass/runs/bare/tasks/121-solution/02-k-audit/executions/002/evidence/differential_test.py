#!/usr/bin/env python3
"""Independent differential test for HumanEval/121 candidate vs canonical."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random
import sys


SCRATCH = Path("/tmp/audit-work/121-solution-audit")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load("trusted_canonical_121", SCRATCH / "reference/canonical.py")
    generated = load("generated_solution_121", SCRATCH / "candidate/solution.py")

    named_cases = [
        ("documented-1", [5, 8, 7, 1]),
        ("documented-2", [3, 3, 3, 3, 3]),
        ("documented-3", [30, 13, 24, 321]),
        ("empty-outside-contract", []),
        ("singleton-even", [0]),
        ("singleton-positive-odd", [1]),
        ("singleton-negative-odd", [-1]),
        ("singleton-negative-even", [-2]),
        ("odd-at-skipped-position", [2, 5]),
        ("odd-at-selected-position", [5, 2]),
        ("both-branches", [-5, 100, -4, 99, 7, 98]),
        ("large-integers", [10**100 + 1, -(10**100 + 2), -(10**100 + 3)]),
    ]

    mismatches: list[tuple[list[int], object, object]] = []
    total = 0

    print("named cases:")
    for name, values in named_cases:
        expected = canonical.solution(values)
        actual = generated.solution(values)
        total += 1
        print(f"  {name}: input={values!r} canonical={expected} generated={actual}")
        if expected != actual:
            mismatches.append((values, expected, actual))

    exhaustive_count = 0
    for length in range(0, 7):
        for values_tuple in itertools.product(range(-3, 4), repeat=length):
            values = list(values_tuple)
            expected = canonical.solution(values)
            actual = generated.solution(values)
            total += 1
            exhaustive_count += 1
            if expected != actual:
                mismatches.append((values, expected, actual))

    rng = random.Random(121_2026_07_26)
    random_count = 5000
    for _ in range(random_count):
        length = rng.randint(1, 40)
        values = [rng.randint(-(10**9), 10**9) for _ in range(length)]
        expected = canonical.solution(values)
        actual = generated.solution(values)
        total += 1
        if expected != actual:
            mismatches.append((values, expected, actual))

    print(
        "generated scope: "
        f"exhaustive lengths=0..6 values=-3..3 cases={exhaustive_count}; "
        f"random seed=12120260726 cases={random_count} lengths=1..40 "
        "values=[-1000000000,1000000000]"
    )
    print(f"total comparisons={total}")
    print(f"mismatches={len(mismatches)}")
    for values, expected, actual in mismatches[:20]:
        print(
            f"MISMATCH input={values!r} canonical={expected!r} generated={actual!r}"
        )
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
