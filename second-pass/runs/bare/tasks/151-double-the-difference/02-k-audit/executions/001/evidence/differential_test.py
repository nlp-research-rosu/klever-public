#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential tests."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import importlib.util
import itertools
import math
from pathlib import Path
import random
from typing import Any


CANONICAL_PATH = Path("/tmp/audit-work/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-src/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.double_the_difference


canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "candidate_solution")


def outcome(function, case: list[Any]) -> tuple[str, Any]:
    try:
        return ("return", function(case))
    except Exception as error:
        return ("raise", (type(error).__name__, str(error)))


def same_outcome(left: tuple[str, Any], right: tuple[str, Any]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "raise":
        return left == right
    left_value = left[1]
    right_value = right[1]
    if isinstance(left_value, float) and isinstance(right_value, float):
        if math.isnan(left_value) and math.isnan(right_value):
            return True
    return left_value == right_value and type(left_value) is type(right_value)


def check_group(name: str, cases: list[list[Any]], require_zero: bool) -> int:
    mismatches: list[
        tuple[int, list[Any], tuple[str, Any], tuple[str, Any]]
    ] = []
    for index, case in enumerate(cases):
        oracle = outcome(canonical, case)
        generated = outcome(candidate, case)
        if not same_outcome(oracle, generated):
            mismatches.append((index, case, oracle, generated))
    print(
        f"GROUP {name}: cases={len(cases)} "
        f"mismatches={len(mismatches)} require_zero={require_zero}"
    )
    for index, case, oracle, generated in mismatches[:20]:
        print(
            f"  mismatch[{index}] input={case!r} "
            f"canonical={oracle!r} candidate={generated!r}"
        )
    if len(mismatches) > 20:
        print(f"  ... {len(mismatches) - 20} further mismatches omitted")
    if require_zero and mismatches:
        raise AssertionError(f"{name} has {len(mismatches)} mismatches")
    return len(mismatches)


def main() -> int:
    documented = [
        [1, 3, 2, 0],
        [-1, -2, 0],
        [9, -2],
        [0],
        [],
    ]
    documented_expected = [10, 0, 81, 0, 0]
    for case, expected in zip(documented, documented_expected):
        actual = candidate(case)
        if actual != expected:
            raise AssertionError(
                f"documented case {case!r}: {actual!r} != {expected!r}"
            )
    check_group("documented_examples", documented, True)

    branch_boundaries = [
        [],
        [-2],
        [-1],
        [0],
        [1],
        [2],
        [3],
        [4],
        [-2, -1, 0, 1, 2, 3, 4],
        [-1.5],
        [-1.0],
        [-0.0],
        [0.0],
        [1.0],
        [1.5],
        [2.0],
        [3.0],
        [True],
        [False],
        [True, False, 1, 2, -1, 3, 1.5],
        [-(10**100), -3, 10**100, 10**100 + 1],
    ]
    check_group("empty_and_branch_boundaries", branch_boundaries, True)

    exhaustive_values: list[Any] = [
        -3,
        -2,
        -1,
        0,
        1,
        2,
        3,
        4,
        -1.5,
        0.0,
        1.0,
        1.5,
        True,
        False,
    ]
    exhaustive_cases: list[list[Any]] = []
    for length in range(5):
        exhaustive_cases.extend(
            [list(items) for items in itertools.product(exhaustive_values, repeat=length)]
        )
    check_group(
        "exhaustive_builtin_finite_values_length_0_through_4",
        exhaustive_cases,
        True,
    )

    rng = random.Random(151_20260726)
    integer_pool = [
        -(10**100),
        -(2**63),
        -101,
        -10,
        -3,
        -2,
        -1,
        0,
        1,
        2,
        3,
        9,
        101,
        2**63 - 1,
        10**100,
        10**100 + 1,
    ]
    float_pool = [
        -1e300,
        -100.25,
        -3.0,
        -1.5,
        -0.0,
        0.0,
        1.0,
        1.5,
        3.0,
        100.25,
        1e300,
    ]
    generated_cases: list[list[Any]] = []
    value_pool = integer_pool + float_pool + [True, False]
    for _ in range(10_000):
        length = rng.randrange(0, 26)
        generated_cases.append([rng.choice(value_pool) for _ in range(length)])
    check_group("seeded_generated_builtin_finite_lists", generated_cases, True)

    # These explicitly expose the trusted canonical's behavior outside the
    # ordinary finite built-in int/float list domain.  They are reported, not
    # silently folded into the zero-mismatch core sample.
    nonfinite_cases = [
        [float("nan")],
        [float("-inf")],
        [float("inf")],
        [1, float("inf"), 3],
    ]
    check_group("reported_nonfinite_float_extension", nonfinite_cases, False)

    alternate_numeric_classes = [
        [Decimal("3")],
        [Decimal("3.0")],
        [Fraction(3, 1)],
        [Fraction(3, 2)],
    ]
    check_group(
        "reported_non_builtin_numeric_classes",
        alternate_numeric_classes,
        False,
    )

    print("CORE_DIFFERENTIAL_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
