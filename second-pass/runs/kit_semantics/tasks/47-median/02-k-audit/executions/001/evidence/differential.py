#!/usr/bin/env python3
"""Independent CPython differential: trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import math
import struct
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", Path("/tmp/audit-work/47-median/trusted/canonical.py"))
generated = load("generated_solution", Path("/tmp/audit-work/47-median/candidate-src/solution.py"))


def outcome(fn: Callable[[list[Any]], Any], values: list[Any]) -> tuple[Any, ...]:
    try:
        value = fn(list(values))
    except Exception as err:  # comparing observable exception classes, not messages
        return ("exception", type(err).__module__, type(err).__qualname__)
    if isinstance(value, float):
        if math.isnan(value):
            return ("value", "float", "nan")
        return ("value", "float", struct.pack(">d", value).hex())
    return ("value", type(value).__module__, type(value).__qualname__, repr(value))


def compare(cases: list[tuple[str, list[Any]]]) -> list[tuple[str, Any, Any]]:
    mismatches = []
    for label, values in cases:
        left = outcome(canonical.median, values)
        right = outcome(generated.median, values)
        if left != right:
            mismatches.append((label, left, right))
    return mismatches


def main() -> int:
    fixed: list[tuple[str, list[Any]]] = [
        ("doc_odd", [3, 1, 2, 4, 5]),
        ("doc_even", [-10, 4, 6, 1000, 10, 20]),
        ("empty", []),
        ("single_int", [7]),
        ("two_int", [2, 1]),
        ("three_duplicates", [2, 2, 2]),
        ("negative_even", [-3, -4, -1, -2]),
        ("single_bool", [True]),
        ("bool_even", [True, False]),
        ("mixed_even", [1.0, 4, 2, 7]),
        ("signed_zero", [-0.0, 0.0]),
        ("infinities", [-math.inf, math.inf]),
        ("nan_first", [math.nan, 1.0, 2.0]),
        ("nan_middle_even", [1.0, math.nan]),
        ("large_exact", [2**53, 2**53 + 2]),
        ("huge_int_divisor_literal_divergence", [10**308, 10**308]),
        ("huge_overflow", [10**400, 10**400]),
        ("single_string", ["é"]),
        ("odd_strings", ["c", "a", "b"]),
        ("even_strings", ["a", "b"]),
        ("incomparable", [1, "a"]),
        ("single_complex", [1 + 2j]),
        ("complex_pair", [1 + 2j, 3 + 4j]),
        ("nested_odd", [[3], [1], [2]]),
        ("nested_even", [[1], [2]]),
    ]
    atoms: list[Any] = [
        -math.inf,
        -2,
        -0.0,
        False,
        0,
        True,
        1.5,
        2**53 + 1,
        math.inf,
        math.nan,
    ]
    generated_cases: list[tuple[str, list[Any]]] = []
    for size in range(1, 4):
        for index, values in enumerate(itertools.product(atoms, repeat=size)):
            generated_cases.append((f"product_{size}_{index}", list(values)))

    intended = fixed + generated_cases
    intended_mismatches = compare(intended)
    print(
        f"builtin_cases={len(intended)} "
        f"builtin_mismatches={len(intended_mismatches)}"
    )
    for mismatch in intended_mismatches[:20]:
        print(f"BUILTIN_MISMATCH {mismatch!r}")

    extension_cases = [
        ("fraction_even", [Fraction(1, 3), Fraction(2, 3)]),
        ("decimal_even", [Decimal("1"), Decimal("2")]),
    ]
    extension_mismatches = compare(extension_cases)
    print(
        f"unrepresented_numeric_cases={len(extension_cases)} "
        f"unrepresented_numeric_mismatches={len(extension_mismatches)}"
    )
    for mismatch in extension_mismatches:
        print(f"UNREPRESENTED_DIVERGENCE {mismatch!r}")

    doc_input = [-10, 4, 6, 1000, 10, 20]
    print(
        "docstring_contradiction "
        f"documented=15.0 canonical={canonical.median(doc_input)!r} "
        f"generated={generated.median(doc_input)!r}"
    )
    gap_input = [10**308, 10**308]
    print(
        "huge_int_python_fidelity "
        f"canonical={outcome(canonical.median, gap_input)!r} "
        f"generated={outcome(generated.median, gap_input)!r}"
    )
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
