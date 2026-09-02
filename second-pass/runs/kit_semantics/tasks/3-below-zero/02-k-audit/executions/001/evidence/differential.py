#!/usr/bin/env python3
"""Independent contract differential for HumanEval/3."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random


SCRATCH = Path("/tmp/audit-work/3-below-zero-audit")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_zero


canonical = load_function("trusted_canonical", SCRATCH / "canonical_ref.py")
generated = load_function("generated_solution", SCRATCH / "solution.py")


def docstring_oracle(operations: list[int]) -> bool:
    balance = 0
    for operation in operations:
        balance = balance + operation
        if balance < 0:
            return True
    return False


fixed_cases = [
    [1, 2, 3],
    [1, 2, -4, 5],
    [],
    [0],
    [-1],
    [1],
    [1, -1],
    [1, -2],
    [-1, 10],
    [10, -10, -1],
    [10**100, -(10**100)],
    [10**100, -(10**100) - 1],
    [-(10**100), 10**100],
]


def cases():
    yield from fixed_cases
    alphabet = range(-3, 4)
    for length in range(7):
        for values in product(alphabet, repeat=length):
            yield list(values)
    rng = random.Random(0x3B3E10)
    for _ in range(5000):
        length = rng.randrange(0, 81)
        yield [rng.randrange(-10**12, 10**12 + 1) for _ in range(length)]


def main() -> None:
    total = 0
    mismatches: list[tuple[list[int], object, object, object]] = []
    for values in cases():
        total += 1
        expected = docstring_oracle(values)
        trusted = canonical(values.copy())
        actual = generated(values.copy())
        if (trusted, actual) != (expected, expected):
            mismatches.append((values, expected, trusted, actual))
            if len(mismatches) >= 20:
                break
    print("oracle=independent running-sum implementation from prompt text")
    print("fixed_cases=13")
    print("exhaustive=lengths 0..6 over integers -3..3")
    print("random=5000 seed=0x3B3E10 lengths 0..80 values -10^12..10^12")
    print(f"cases_checked={total}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
