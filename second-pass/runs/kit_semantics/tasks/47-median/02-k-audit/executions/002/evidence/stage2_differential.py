#!/usr/bin/env python3
"""Docstring-first differential for HumanEval 47-median.

The candidate and trusted canonical are loaded from the mounted copies placed
in the fresh audit scratch tree.  statistics.median is an independent standard
library witness for the ordinary mathematical reading of "median".
"""

from __future__ import annotations

import importlib.util
import math
import random
import statistics
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/median47")


def load_function(path: Path, module_name: str) -> Callable[[list], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


CANDIDATE = load_function(SCRATCH / "solution.py", "audit_candidate")
CANONICAL = load_function(SCRATCH / "canonical.py", "audit_canonical")


@dataclass(frozen=True)
class Outcome:
    kind: str
    type_name: str
    value: str


def run(function: Callable[[list], Any], values: list) -> Outcome:
    try:
        result = function(list(values))
    except Exception as err:  # The exception class and message are observations.
        return Outcome("exception", type(err).__name__, str(err))
    return Outcome("return", type(result).__name__, repr(result))


def semantic_equal(left: Outcome, right: Outcome) -> bool:
    if left.kind != right.kind or left.type_name != right.type_name:
        return False
    if left.kind == "exception":
        return True
    if left.value == right.value:
        return True
    return left.type_name == "float" and left.value == "nan" and right.value == "nan"


def values_equal(left: Any, right: Any) -> bool:
    try:
        if isinstance(left, float) and isinstance(right, float):
            if math.isnan(left) and math.isnan(right):
                return True
        return type(left) is type(right) and left == right
    except Exception:
        return False


def independent_oracle(values: list) -> Outcome:
    return run(statistics.median, values)


def emit_case(case_id: str, values: list) -> tuple[bool, bool]:
    candidate = run(CANDIDATE, values)
    canonical = run(CANONICAL, values)
    oracle = independent_oracle(values)
    cc_equal = semantic_equal(candidate, canonical)
    co_equal = semantic_equal(candidate, oracle)
    print(
        f"CASE {case_id} input={values!r} "
        f"candidate={candidate} canonical={canonical} oracle={oracle} "
        f"candidate_eq_canonical={cc_equal} candidate_eq_oracle={co_equal}"
    )
    return cc_equal, co_equal


def main() -> int:
    fixed_cases: list[tuple[str, list]] = [
        ("doc_odd", [3, 1, 2, 4, 5]),
        ("doc_even_contradiction", [-10, 4, 6, 1000, 10, 20]),
        ("empty", []),
        ("length_1_int", [7]),
        ("length_2_int", [1, 9]),
        ("length_3_int", [3, 1, 2]),
        ("length_4_int", [4, 1, 3, 2]),
        ("duplicates", [2, 2, 2, 2]),
        ("negative_even", [-9, -1, -3, -7]),
        ("large_int", [10**100, 10**100 + 2]),
        ("bool_bool", [False, True]),
        ("int_bool", [0, True]),
        ("bool_int", [False, 3]),
        ("float_float", [1.25, 3.75]),
        ("int_float", [1, 2.5]),
        ("float_int", [1.5, 4]),
        ("bool_float", [False, 4.0]),
        ("float_bool", [1.0, True]),
        ("odd_strings", ["c", "a", "b"]),
        ("even_strings", ["d", "a", "c", "b"]),
        ("incomparable", [1, "a"]),
        ("signed_zero", [-0.0, 0.0]),
        ("positive_infinity", [1.0, float("inf")]),
        ("negative_infinity", [float("-inf"), 1.0]),
        ("opposite_infinities", [float("-inf"), float("inf")]),
        ("nan_first", [float("nan"), 1.0, 2.0]),
        ("nan_center", [1.0, float("nan"), 2.0]),
        ("fraction_even", [Fraction(1, 3), Fraction(2, 3)]),
        ("decimal_even", [Decimal("1.0"), Decimal("2.0")]),
    ]

    canonical_mismatches: list[str] = []
    oracle_mismatches: list[str] = []
    for case_id, values in fixed_cases:
        cc_equal, co_equal = emit_case(case_id, values)
        if not cc_equal:
            canonical_mismatches.append(case_id)
        if not co_equal:
            oracle_mismatches.append(case_id)

    rng = random.Random(470047)
    generated: list[tuple[str, list]] = []
    numeric_pool: list[Any] = [
        -100,
        -10,
        -1,
        0,
        1,
        2,
        10,
        100,
        False,
        True,
        -3.5,
        -0.0,
        0.25,
        2.5,
        99.0,
    ]
    for index in range(240):
        length = rng.randint(1, 12)
        if index < 120:
            values = [rng.randint(-10_000, 10_000) for _ in range(length)]
        else:
            values = [rng.choice(numeric_pool) for _ in range(length)]
        generated.append((f"generated_{index:03d}", values))

    for case_id, values in generated:
        cc_equal, co_equal = emit_case(case_id, values)
        if not cc_equal:
            canonical_mismatches.append(case_id)
        if not co_equal:
            oracle_mismatches.append(case_id)

    doc_odd = CANDIDATE([3, 1, 2, 4, 5])
    doc_even = CANDIDATE([-10, 4, 6, 1000, 10, 20])
    print(
        "DOCSTRING_CHECK "
        f"odd_expected=3 odd_actual={doc_odd!r} odd_match={values_equal(doc_odd, 3)} "
        f"even_written_expected=15.0 even_actual={doc_even!r} "
        f"even_written_match={values_equal(doc_even, 15.0)} "
        "even_sorted_centers=(6,10) conventional_expected=8.0 "
        f"conventional_match={values_equal(doc_even, 8.0)}"
    )
    print(
        f"SUMMARY fixed={len(fixed_cases)} generated={len(generated)} "
        f"candidate_canonical_mismatches={canonical_mismatches} "
        f"candidate_oracle_mismatches={oracle_mismatches}"
    )

    # The docstring's first example and ordinary median reading must hold.
    # The second literal expected value is intentionally reported, not enforced,
    # because its own sorted-center arithmetic contradicts it.
    return 0 if values_equal(doc_odd, 3) and values_equal(doc_even, 8.0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
