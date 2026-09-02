#!/usr/bin/env python3
"""Independent differential check of trusted canonical.py and solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import math
import random
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work/scratch/proof")
INPUT_RECORD = Path("/audit-output/evidence/stage2/differential-inputs.txt")


def load_function(path: Path, module_name: str) -> Callable[..., str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


def outcome(function: Callable[..., str], left: list[Any], right: list[Any]):
    try:
        return ("return", function(list(left), list(right)))
    except Exception as error:  # Differentially compare behavior, including errors.
        return ("raise", type(error).__name__, str(error))


def main() -> None:
    canonical = load_function(WORK / "canonical.py", "trusted_canonical")
    generated = load_function(WORK / "solution.py", "generated_solution")

    explicit: list[tuple[list[Any], list[Any], str | None, str]] = [
        ([1, 2, 3, 4], [1, 2, 3, 4], "YES", "documented-example-yes"),
        ([1, 2, 3, 4], [1, 5, 3, 4], "NO", "documented-example-no"),
        ([], [], "YES", "both-empty-outside-precondition"),
        ([], [1], "YES", "empty-lst1-outside-precondition"),
        ([1], [], "NO", "empty-lst2-outside-precondition"),
        ([2], [1], "YES", "one-even-at-threshold"),
        ([1], [2], "YES", "exchange-at-threshold"),
        ([1], [1], "NO", "one-below-threshold"),
        ([1, 3, 2], [5, 4], "NO", "combined-even-count-len-minus-one"),
        ([1, 3, 2], [4, 6], "YES", "combined-even-count-equals-len"),
        ([2, 4, 6], [8], "YES", "combined-even-count-above-len"),
        ([-4, -3], [-2], "YES", "negative-even-boundary"),
        ([True, False], [True, False], "YES", "bool-numeric-behavior"),
        ([2.0, 3.5], [4.0], "YES", "finite-float-boundary"),
        ([2.5, -3.5], [4.25], "NO", "nonintegral-floats"),
        ([10**100 + 1], [-(10**100)], "YES", "unbounded-python-int"),
        ([float("nan")], [2.0], "YES", "nan-with-one-even"),
        ([float("inf")], [2.0], None, "positive-infinity"),
        ([float("-inf")], [2.0], None, "negative-infinity"),
        ([Decimal("2.0")], [Decimal("1.0")], "YES", "decimal-extension"),
        ([Fraction(3, 2)], [Fraction(4, 1)], "YES", "fraction-extension"),
    ]

    cases: list[tuple[list[Any], list[Any], str | None, str]] = list(explicit)

    small_values = [-2, -1, 0, 1, 2]
    small_lists: list[list[int]] = [[]]
    for length in range(1, 4):
        frontier = [[]]
        for _ in range(length):
            frontier = [prefix + [value] for prefix in frontier for value in small_values]
        small_lists.extend(frontier)
    for left in small_lists:
        for right in small_lists:
            cases.append((left, right, None, "exhaustive-small-int"))

    seed = 11020260729
    randomizer = random.Random(seed)
    pool: list[Any] = [
        -10**30,
        -7,
        -4,
        -1,
        0,
        1,
        2,
        5,
        10**30,
        False,
        True,
        -4.0,
        -3.5,
        -0.0,
        0.25,
        2.0,
        6.5,
        float("nan"),
        float("inf"),
        float("-inf"),
    ]
    for _ in range(5000):
        left = [randomizer.choice(pool) for _ in range(randomizer.randint(1, 12))]
        right = [randomizer.choice(pool) for _ in range(randomizer.randint(1, 12))]
        cases.append((left, right, None, "seeded-mixed-numeric"))

    input_lines = [
        f"{index:05d}\t{tag}\tleft={left!r}\tright={right!r}\texpected={expected!r}"
        for index, (left, right, expected, tag) in enumerate(cases)
    ]
    input_text = "\n".join(input_lines) + "\n"
    INPUT_RECORD.write_text(input_text)
    input_hash = hashlib.sha256(input_text.encode()).hexdigest()

    mismatches = []
    expectation_failures = []
    explicit_results = []
    for index, (left, right, expected, tag) in enumerate(cases):
        oracle = outcome(canonical, left, right)
        observed = outcome(generated, left, right)
        if oracle != observed:
            mismatches.append((index, tag, left, right, oracle, observed))
        if expected is not None and oracle != ("return", expected):
            expectation_failures.append((index, tag, expected, oracle))
        if index < len(explicit):
            explicit_results.append((index, tag, oracle, observed))

    print("oracle=/tmp/audit-work/scratch/proof/canonical.py")
    print("candidate=/tmp/audit-work/scratch/proof/solution.py")
    print(f"seed={seed}")
    print(f"cases={len(cases)}")
    print(f"inputs_sha256={input_hash}")
    print(f"input_record={INPUT_RECORD}")
    print(f"mismatches={len(mismatches)}")
    print(f"expectation_failures={len(expectation_failures)}")
    print("explicit_results:")
    for item in explicit_results:
        print(repr(item))
    for item in mismatches[:20]:
        print("MISMATCH", repr(item))
    for item in expectation_failures[:20]:
        print("EXPECTATION_FAILURE", repr(item))

    if mismatches or expectation_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
