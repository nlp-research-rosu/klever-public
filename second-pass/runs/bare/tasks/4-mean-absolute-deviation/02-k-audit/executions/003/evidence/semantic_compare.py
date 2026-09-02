#!/usr/bin/env python3
"""Compare fresh K concrete results with independent Python/Fraction execution."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
from pathlib import Path
import re
from typing import Any


EVIDENCE = Path("/audit-output/evidence")
SOLUTION = Path("/tmp/audit-work/4-mad-audit/candidate/solution.py")


def load_solution():
    spec = importlib.util.spec_from_file_location("semantic_compare_solution", SOLUTION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def k_rat(log_name: str) -> tuple[int, int]:
    text = (EVIDENCE / log_name).read_text(encoding="utf-8")
    matches = re.findall(r"result\s*\(\s*rat\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*\)", text)
    if len(matches) != 1:
        raise ValueError(f"{log_name}: expected one final result, found {matches!r}")
    return tuple(map(int, matches[0]))


def python_outcome(function, values: list[Any]):
    try:
        return ("value", function(list(values)))
    except BaseException as err:
        return ("exception", type(err).__qualname__, err.args)


def compare_fraction(function, label: str, log_name: str, values: list[Fraction]) -> bool:
    numerator, denominator = k_rat(log_name)
    k_value = Fraction(numerator, denominator)
    python_value = python_outcome(function, values)
    expected = python_value[1] if python_value[0] == "value" else None
    same = python_value[0] == "value" and k_value == expected
    print(
        f"{label}: input={values!r} k_raw=rat({numerator},{denominator}) "
        f"k_fraction={k_value!r} python={python_value!r} same={same}"
    )
    return same


def main() -> int:
    function = load_solution()
    expected_agreements = [
        compare_fraction(
            function,
            "documented-example",
            "03-krun-example.log",
            list(map(Fraction, [1, 2, 3, 4])),
        ),
        compare_fraction(
            function,
            "singleton",
            "03-krun-singleton.log",
            [Fraction(5)],
        ),
        compare_fraction(
            function,
            "abs-branch-boundaries",
            "03-krun-abs-boundaries.log",
            list(map(Fraction, [-2, 0, 2])),
        ),
        compare_fraction(
            function,
            "decimal-rationals",
            "03-krun-decimal-rationals.log",
            [Fraction(1, 10), Fraction(2, 10), Fraction(3, 10)],
        ),
    ]

    empty_k = k_rat("03-krun-empty-valid.log")
    empty_python = python_outcome(function, [])
    empty_same = empty_python[0] == "value"
    print(
        f"empty-boundary: k_raw=rat{empty_k!r} k_terminated=True "
        f"python={empty_python!r} same={empty_same}"
    )

    negative_denominator_same = compare_fraction(
        function,
        "negative-denominator-representation",
        "03-krun-negative-denominator.log",
        [Fraction(1, -1), Fraction(1, 1)],
    )

    binary_inputs = [0.1, 0.2, 0.3]
    encoded = [Fraction.from_float(value) for value in binary_inputs]
    numerator, denominator = k_rat("03-krun-binary-float-encoding.log")
    k_binary = Fraction(numerator, denominator)
    python_binary_float = function(binary_inputs)
    python_binary_exact = Fraction.from_float(python_binary_float)
    binary_same = k_binary == python_binary_exact
    print(
        "binary-float-encoding: "
        f"input={binary_inputs!r} encoded={encoded!r} "
        f"k_fraction={k_binary!r} python_float={python_binary_float!r} "
        f"python_float_exact={python_binary_exact!r} same={binary_same} "
        f"difference={k_binary - python_binary_exact!r}"
    )

    print(f"positive_denominator_agreements={sum(expected_agreements)}/{len(expected_agreements)}")
    print(
        "expected_mismatches: "
        f"empty={not empty_same} negative_denominator={not negative_denominator_same} "
        f"binary_float_rounding={not binary_same}"
    )
    return 0 if all(expected_agreements) and not empty_same and not negative_denominator_same and not binary_same else 1


if __name__ == "__main__":
    raise SystemExit(main())
