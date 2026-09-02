#!/usr/bin/env python3
"""Independent differential test of trusted canonical vs candidate Python."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path
from typing import Callable


def load_count_nums(module_name: str, path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_nums


def outcome(function: Callable[[list[int]], int], values: list[int]) -> tuple[str, object]:
    try:
        return ("return", function(values.copy()))
    except Exception as error:  # Deliberately compare exceptional behavior too.
        return ("raise", type(error).__name__)


def main() -> int:
    canonical = load_count_nums("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_count_nums(
        "scratch_candidate", Path("/tmp/audit-work/108-count-nums/solution.py")
    )

    named: list[tuple[str, list[int]]] = [
        ("example_empty", []),
        ("example_mixed", [-1, 11, -11]),
        ("example_positive", [1, 1, 2]),
        ("all_digit_branches", [-123, -100, -99, -10, -9, -1, 0, 1, 9, 10, 11]),
        ("zero_sum_boundaries", [-99, -11, 0]),
        ("positive_signed_negative", [-123, -12]),
        ("singleton_min_branch", [-10]),
        ("singleton_neg_base", [-9]),
        ("singleton_pos_base", [9]),
        ("singleton_max_branch", [10]),
    ]

    alphabet = [-123, -100, -99, -12, -11, -10, -9, -1, 0, 1, 9, 10, 11, 99, 100]
    generated: list[tuple[str, list[int]]] = []
    for length in range(4):
        for index, values in enumerate(itertools.product(alphabet, repeat=length)):
            generated.append((f"exhaustive_l{length}_{index}", list(values)))

    rng = random.Random(108)
    for index in range(500):
        length = rng.randrange(0, 31)
        values = [rng.randrange(-(10**50), 10**50) for _ in range(length)]
        generated.append((f"random_{index}", values))

    mismatches: list[tuple[str, tuple[str, object], tuple[str, object]]] = []
    for name, values in named + generated:
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        if expected != actual:
            mismatches.append((name, expected, actual))

    # Unrestricted source-contract witnesses: both are lists of Python integers.
    depth_witnesses = [
        ("long_list_1200", [1] * 1200),
        ("long_integer_1200_digits", [10**1199]),
    ]
    for name, values in depth_witnesses:
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        print(f"DEPTH_WITNESS {name} canonical={expected} candidate={actual}")
        if expected != actual:
            mismatches.append((name, expected, actual))

    ordinary_count = len(named) + len(generated)
    ordinary_mismatches = [
        mismatch for mismatch in mismatches if not mismatch[0].startswith("long_")
    ]
    print(f"ORDINARY_CASES {ordinary_count}")
    print(f"ORDINARY_MISMATCHES {len(ordinary_mismatches)}")
    print(f"TOTAL_MISMATCHES {len(mismatches)}")
    for name, expected, actual in mismatches:
        print(f"MISMATCH {name} canonical={expected} candidate={actual}")

    # The script succeeds when its observations are internally as expected:
    # no ordinary arithmetic mismatch, and both recursion-depth divergences found.
    assert not ordinary_mismatches
    assert {item[0] for item in mismatches} == {
        "long_list_1200",
        "long_integer_1200_digits",
    }
    return 0


if __name__ == "__main__":
    sys.exit(main())
