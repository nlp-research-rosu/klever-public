#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval 157."""

from __future__ import annotations

import decimal
import fractions
import importlib.util
import itertools
import math
import random
from pathlib import Path
from typing import Any


CANONICAL = Path("/tmp/audit-work/reconstruction/canonical.py")
CANDIDATE = Path("/tmp/audit-work/reconstruction/solution.py")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


def outcome(function, args: tuple[Any, ...]) -> tuple[Any, ...]:
    try:
        value = function(*args)
        return ("return", type(value).__qualname__, value)
    except Exception as error:  # This is an exception-equivalence boundary test.
        return ("raise", type(error).__qualname__, error.args)


def same_outcome(left: tuple[Any, ...], right: tuple[Any, ...]) -> bool:
    if left[:2] != right[:2]:
        return False
    if left[0] == "raise":
        return left == right
    left_value = left[2]
    right_value = right[2]
    if isinstance(left_value, float) and isinstance(right_value, float):
        if math.isnan(left_value) and math.isnan(right_value):
            return True
    return left_value == right_value


def main() -> None:
    canonical = load_function(CANONICAL, "trusted_canonical")
    candidate = load_function(CANDIDATE, "audited_candidate")

    categories: dict[str, list[tuple[Any, ...]]] = {
        "documented_examples": [(3, 4, 5), (1, 2, 3)],
        "branch_and_boundary": [
            (5, 3, 4),      # first equality true
            (3, 5, 4),      # second equality true
            (3, 4, 5),      # third equality true
            (2, 2, 3),      # all false
            (0, 0, 0),      # arithmetic boundary
            (-3, -4, -5),   # signs do not affect squares
            (1, 1, 1),
            (2**53, 0, 2**53),
            (10**100, 0, 10**100),
            (True, False, True),
        ],
        "arity_boundaries": [(), (3,), (3, 4), (3, 4, 5, 6)],
        "model_gap_numeric_classes": [
            (
                fractions.Fraction(3),
                fractions.Fraction(4),
                fractions.Fraction(5),
            ),
            (
                decimal.Decimal("3"),
                decimal.Decimal("4"),
                decimal.Decimal("5"),
            ),
            (3 + 0j, 4 + 0j, 5 + 0j),
        ],
    }

    categories["exhaustive_small_ints"] = list(
        itertools.product(range(-12, 13), repeat=3)
    )

    float_values = [
        -math.inf,
        -float.fromhex("0x1.fffffffffffffp+1023"),
        -2.5,
        -1.0,
        -0.0,
        0.0,
        float.fromhex("0x0.0000000000001p-1022"),
        0.1,
        0.3,
        0.4,
        0.5,
        1.0,
        1.5,
        2.0,
        2.5,
        float.fromhex("0x1.fffffffffffffp+1023"),
        math.inf,
        math.nan,
    ]
    categories["float_cartesian"] = list(itertools.product(float_values, repeat=3))

    mixed_values = [-3, -0.0, 0, 0.5, 1, 2.0, 3, 4.0, 5, math.inf, math.nan]
    categories["mixed_cartesian"] = list(itertools.product(mixed_values, repeat=3))

    rng = random.Random(157)
    random_cases: list[tuple[Any, ...]] = []
    for _ in range(10_000):
        args: list[Any] = []
        for _position in range(3):
            if rng.randrange(2):
                args.append(rng.randint(-(10**12), 10**12))
            else:
                args.append(rng.uniform(-10**6, 10**6))
        random_cases.append(tuple(args))
    categories["deterministic_random_mixed"] = random_cases

    mismatches: list[tuple[str, tuple[Any, ...], tuple[Any, ...], tuple[Any, ...]]] = []
    total = 0
    for category, cases in categories.items():
        category_mismatches = 0
        for args in cases:
            total += 1
            expected = outcome(canonical, args)
            actual = outcome(candidate, args)
            if not same_outcome(expected, actual):
                category_mismatches += 1
                if len(mismatches) < 20:
                    mismatches.append((category, args, expected, actual))
        print(
            f"CATEGORY {category} cases={len(cases)} "
            f"mismatches={category_mismatches}"
        )

    print(f"TOTAL cases={total} mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches:
            print(f"MISMATCH {mismatch!r}")
        raise AssertionError("canonical/candidate differential mismatch")

    gap_witness = categories["model_gap_numeric_classes"][0]
    print(
        "MODEL_GAP_WITNESS "
        f"input={gap_witness!r} "
        f"cpython_canonical={outcome(canonical, gap_witness)!r} "
        "mpy_representation=absent"
    )


if __name__ == "__main__":
    main()
