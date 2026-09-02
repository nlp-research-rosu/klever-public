#!/usr/bin/env python3
"""Independent differential check for HumanEval/146 on its integer-list domain."""

from __future__ import annotations

import importlib.util
import itertools
import pathlib
import random
import sys


SCRATCH = pathlib.Path("/tmp/audit-work")
ODD_DIGITS = frozenset("13579")


def load_entry(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.specialFilter


def independent_oracle(nums: list[int]) -> int:
    count = 0
    for value in nums:
        if value <= 10:
            continue
        decimal = str(value)
        if decimal[0] in ODD_DIGITS and decimal[-1] in ODD_DIGITS:
            count += 1
    return count


def main() -> int:
    canonical = load_entry("audit_canonical", SCRATCH / "canonical.py")
    generated = load_entry("audit_generated", SCRATCH / "solution.py")

    named_cases: list[tuple[str, list[int]]] = [
        ("doc-example-1", [15, -73, 14, -15]),
        ("doc-example-2", [33, -2, -3, 45, 21, 109]),
        ("empty", []),
        ("threshold", [9, 10, 11, 12]),
        ("first-even-last-odd", [21, 23, 25, 27, 29]),
        ("first-odd-last-even", [12, 14, 16, 18, 32, 34]),
        ("both-odd", [11, 13, 15, 17, 19, 31, 33, 35, 37, 39]),
        ("both-even", [20, 22, 24, 26, 28]),
        ("negative-and-zero", [-999, -15, -11, -10, -1, 0]),
        ("repeated-values", [11, 11, 12, 11, 12, 11]),
        ("long-integers", [10**999 + 1, 3 * 10**999 + 9, 8 * 10**999 + 7]),
    ]

    # Exhaust every branch for singleton inputs across a broad contiguous range.
    cases: list[tuple[str, list[int]]] = list(named_cases)
    cases.extend((f"singleton-{n}", [n]) for n in range(-1000, 10001))

    # Exhaustively combine representative values at lengths 0 through 4.
    representatives = [-73, 10, 11, 12, 19, 20, 21, 33, 45, 109, 24681]
    for length in range(5):
        for index, values in enumerate(itertools.product(representatives, repeat=length)):
            cases.append((f"product-{length}-{index}", list(values)))

    # Deterministic broader input lists and arbitrarily large Python integers.
    rng = random.Random(0x146)
    for index in range(2000):
        length = rng.randrange(0, 65)
        values = [
            rng.randrange(-(10 ** rng.randrange(1, 151)), 10 ** rng.randrange(1, 151))
            for _ in range(length)
        ]
        cases.append((f"random-{index}", values))

    mismatches: list[tuple[str, object, object, object]] = []
    for name, nums in cases:
        expected = independent_oracle(nums)
        trusted = canonical(nums)
        actual = generated(nums)
        if trusted != expected or actual != expected:
            mismatches.append((name, trusted, actual, expected))

    print(f"python={sys.version.split()[0]}")
    print(f"named_cases={len(named_cases)}")
    print("singleton_range=-1000..10000")
    print(f"product_cases={sum(len(representatives) ** n for n in range(5))}")
    print("random_seed=0x146 random_cases=2000 lengths=0..64 magnitudes=1..150 digits")
    print(f"total_cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print("MISMATCH", repr(mismatch))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
