#!/usr/bin/env python3
"""Independent differential check for HumanEval 9 rolling_max."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path
from typing import Callable, Iterable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/9-rolling-max/build/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rolling_max


def independent_oracle(numbers: list[int]) -> list[int]:
    result: list[int] = []
    for index in range(len(numbers)):
        result.append(max(numbers[: index + 1]))
    return result


def exhaustive_inputs() -> Iterable[list[int]]:
    alphabet = (-3, -1, 0, 1, 3)
    for length in range(7):
        for values in itertools.product(alphabet, repeat=length):
            yield list(values)


def generated_inputs() -> Iterable[list[int]]:
    rng = random.Random(0x9A11D17)
    for _ in range(2000):
        length = rng.randrange(0, 31)
        yield [rng.randrange(-10**9, 10**9 + 1) for _ in range(length)]


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "submitted_generated")

    named_cases = {
        "documented-example": [1, 2, 3, 2, 3, 4, 2],
        "empty": [],
        "singleton-zero": [0],
        "singleton-negative": [-7],
        "first-then-less": [2, 1],
        "first-then-greater": [1, 2],
        "equal-comparison-boundary": [2, 2],
        "all-negative": [-5, -9, -3, -4],
        "alternating-extremes": [10**100, -(10**100), 10**100 + 1],
        "duplicates-after-rise": [-1, 0, 0, -1, 3, 3],
    }

    mismatches: list[tuple[str, list[int], object, object, object]] = []
    tested = 0

    def check(label: str, values: list[int]) -> None:
        nonlocal tested
        original = list(values)
        canonical_result = canonical(values)
        generated_result = generated(values)
        oracle_result = independent_oracle(values)
        tested += 1
        if (
            canonical_result != generated_result
            or canonical_result != oracle_result
            or values != original
        ):
            mismatches.append(
                (label, original, canonical_result, generated_result, oracle_result)
            )

    for label, values in named_cases.items():
        check(label, values)
        print(
            f"NAMED {label}: input={values!r} "
            f"canonical={canonical(values)!r} generated={generated(values)!r}"
        )

    exhaustive_count = 0
    for values in exhaustive_inputs():
        check("exhaustive", values)
        exhaustive_count += 1

    generated_count = 0
    for values in generated_inputs():
        check("generated-seed-0x9A11D17", values)
        generated_count += 1

    print(
        "SCOPE: named=10; exhaustive=all lists of lengths 0..6 over "
        "{-3,-1,0,1,3}; generated=2000 lists of lengths 0..30 with values "
        "in [-10^9,10^9], seed=0x9A11D17"
    )
    print(
        f"SUMMARY: total={tested} exhaustive={exhaustive_count} "
        f"generated={generated_count} mismatches={len(mismatches)}"
    )
    for mismatch in mismatches[:20]:
        print(f"MISMATCH: {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
