#!/usr/bin/env python3
"""Independent differential and exact-contract tests for closest_integer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Callable


def load_function(path: str, module_name: str) -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


canonical = load_function("/reference/canonical.py", "trusted_canonical")
generated = load_function(
    "/tmp/audit-work/candidate-src/solution.py", "generated_solution"
)


def outcome(function: Callable[[str], int], value: str) -> tuple[str, Any]:
    try:
        return ("return", function(value))
    except Exception as err:  # Compare the observable exception class.
        return ("raise", type(err).__name__)


def contract_outcome(value: str) -> tuple[str, Any]:
    """Interpret the prompt's string as a decimal number, without binary loss."""
    try:
        number = Decimal(value)
        if not number.is_finite():
            return ("outside", "non-finite")
        return ("return", int(number.to_integral_value(rounding=ROUND_HALF_UP)))
    except (InvalidOperation, ValueError):
        return ("outside", "not-a-number-string")


explicit = [
    # Documented examples.
    "10",
    "15.3",
    "14.5",
    "-14.5",
    # Empty/invalid and exact zero boundaries.
    "",
    ".",
    "+",
    "-",
    "0",
    "-0",
    "+0",
    "0.0",
    "-0.0",
    "0.000",
    # Both sides and both branches around the half boundary.
    "0.49",
    "0.4999999999999999",
    "0.5",
    "0.5000000000000001",
    "-0.49",
    "-0.4999999999999999",
    "-0.5",
    "-0.5000000000000001",
    "1.4999999999999998",
    "1.5",
    "1.5000000000000002",
    "-1.4999999999999998",
    "-1.5",
    "-1.5000000000000002",
    "2.4999999999999999999999999999999999",
    "2.5000000000000000000000000000000001",
    "-2.4999999999999999999999999999999999",
    "-2.5000000000000000000000000000000001",
    # Alternate accepted spellings and trailing zeros.
    "2.50",
    "-2.50",
    "  3.5  ",
    "+4.5",
    "1e1",
    "1.5e1",
    "-1.5e1",
    "1e-1",
    # Binary64 precision boundaries.
    "4503599627370495.5",
    "4503599627370496.5",
    "-4503599627370495.5",
    "-4503599627370496.5",
    "9007199254740991",
    "9007199254740992",
    "9007199254740993",
    "-9007199254740993",
]

generated_cases: list[str] = []
for integer in range(-12, 13):
    sign = "-" if integer < 0 else ""
    magnitude = abs(integer)
    generated_cases.extend(
        [
            f"{sign}{magnitude}.499999999999999999",
            f"{sign}{magnitude}.500000000000000000",
            f"{sign}{magnitude}.500000000000000001",
        ]
    )

rng = random.Random(990026)
for _ in range(100):
    sign = "-" if rng.randrange(2) else ""
    whole = rng.randrange(0, 100000)
    fraction = rng.randrange(0, 10**12)
    generated_cases.append(f"{sign}{whole}.{fraction:012d}")

cases = list(dict.fromkeys(explicit + generated_cases))
encoded_inputs = json.dumps(cases, separators=(",", ":"), ensure_ascii=True)
print(f"INPUT_COUNT={len(cases)}")
print(f"INPUTS_SHA256={hashlib.sha256(encoded_inputs.encode()).hexdigest()}")
for index, value in enumerate(cases):
    print(f"INPUT[{index}]={value!r}")

canonical_mismatches: list[tuple[str, Any, Any]] = []
contract_mismatches: list[tuple[str, Any, Any]] = []
canonical_contract_mismatches: list[tuple[str, Any, Any]] = []
for value in cases:
    expected = outcome(canonical, value)
    actual = outcome(generated, value)
    contract = contract_outcome(value)
    if expected != actual:
        canonical_mismatches.append((value, expected, actual))
    if contract[0] != "outside" and contract != actual:
        contract_mismatches.append((value, contract, actual))
    if contract[0] != "outside" and contract != expected:
        canonical_contract_mismatches.append((value, contract, expected))

for label, mismatches in [
    ("GENERATED_VS_CANONICAL", canonical_mismatches),
    ("GENERATED_VS_PROMPT_DECIMAL", contract_mismatches),
    ("CANONICAL_VS_PROMPT_DECIMAL", canonical_contract_mismatches),
]:
    print(f"{label}_MISMATCH_COUNT={len(mismatches)}")
    for value, expected, actual in mismatches[:20]:
        print(
            f"{label}_MISMATCH value={value!r} expected={expected!r} actual={actual!r}"
        )

documented = ["10", "15.3", "14.5", "-14.5"]
assert all(outcome(generated, value) == contract_outcome(value) for value in documented)
print("DOCUMENTED_EXAMPLES_PASS=true")

if canonical_mismatches or contract_mismatches:
    print("DIFFERENTIAL_RESULT=MISMATCH")
    sys.exit(1)
print("DIFFERENTIAL_RESULT=PASS")
