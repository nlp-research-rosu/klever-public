#!/usr/bin/env python3
"""Independent differential test for HumanEval 94.

The mathematical oracle is separate from both implementations.  The test
intentionally records canonical/reference discrepancies rather than hiding
them, because the natural-language contract excludes 1 from the primes.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path
import random
from typing import Callable


ROOT = Path("/tmp/audit-work/reconstruction")


def load_function(path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(path.stem + "_audit", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.skjkasdkd


def is_prime_math(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def oracle(values: list[int]) -> int:
    primes = [value for value in values if is_prime_math(value)]
    if not primes:
        return 0
    return sum(int(digit) for digit in str(max(primes)))


def main() -> None:
    generated = load_function(ROOT / "solution.py")
    canonical = load_function(ROOT / "canonical.py")

    examples = [
        ([0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3], 10),
        ([1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1], 25),
        ([1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3], 13),
        ([0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6], 11),
        ([0, 81, 12, 3, 1, 21], 3),
        ([0, 8, 1, 2, 1, 7], 7),
    ]
    boundaries = [
        [],
        [-5, -2, -1],
        [0],
        [1],
        [0, 1],
        [2],
        [3],
        [4],
        [2, 2],
        [2, 1],
        [1, 2],
        [3, 4],
        [4, 3],
        [4, 5],
        [5, 4],
        [8, 9, 25, 49],
        [97, 101, 99],
        [101, 103, 107],
        [9973, 10000],
        [99991, 99989],
    ]

    print("DOCUMENTED EXAMPLES")
    for values, expected in examples:
        got = generated(values)
        ref = canonical(values)
        independent = oracle(values)
        print(
            f"input={values!r} expected={expected} "
            f"generated={got} canonical={ref} oracle={independent}"
        )
        assert got == expected == independent
        assert ref == expected

    print("BOUNDARY AND BRANCH CASES")
    for values in boundaries:
        got = generated(values)
        ref = canonical(values)
        independent = oracle(values)
        print(
            f"input={values!r} generated={got} "
            f"canonical={ref} oracle={independent}"
        )
        assert got == independent

    generated_mismatches: list[tuple[list[int], int, int]] = []
    canonical_mismatches: list[tuple[list[int], int, int]] = []
    total = 0

    # Exhaust every list of length 0..3 over values spanning negative,
    # 0/1, the first primes, squares, and composites.
    exhaustive_values = list(range(-3, 16))
    for length in range(4):
        for item in itertools.product(exhaustive_values, repeat=length):
            values = list(item)
            expected = oracle(values)
            got = generated(values)
            ref = canonical(values)
            total += 1
            if got != expected:
                generated_mismatches.append((values, got, expected))
            if ref != expected:
                canonical_mismatches.append((values, ref, expected))

    # Deterministic broader representative lists and larger prime/composite
    # boundaries.
    rng = random.Random(940026)
    for _ in range(3000):
        values = [
            rng.randint(-100, 100_000)
            for _ in range(rng.randint(0, 25))
        ]
        expected = oracle(values)
        got = generated(values)
        ref = canonical(values)
        total += 1
        if got != expected:
            generated_mismatches.append((values, got, expected))
        if ref != expected:
            canonical_mismatches.append((values, ref, expected))

    print("SUMMARY")
    print(f"generated_cases={total + len(examples) + len(boundaries)}")
    print(f"generated_vs_oracle_mismatches={len(generated_mismatches)}")
    print(f"canonical_vs_oracle_mismatches={len(canonical_mismatches)}")
    print("first_canonical_mismatches:")
    for mismatch in canonical_mismatches[:12]:
        print(mismatch)

    assert not generated_mismatches
    # The trusted dataset implementation treats 1 as prime.  Check that every
    # observed mismatch has exactly that known shape.
    assert canonical_mismatches
    for values, ref, expected in canonical_mismatches:
        assert 1 in values
        assert not any(is_prime_math(value) for value in values)
        assert ref == 1 and expected == 0
    print("PASS: generated implementation matches the natural-language oracle")
    print(
        "OBSERVATION: canonical differs only on sampled no-prime lists "
        "containing 1"
    )


if __name__ == "__main__":
    main()
