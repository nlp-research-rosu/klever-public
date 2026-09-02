#!/usr/bin/env python3
"""Independent canonical/candidate differential test for HumanEval 99."""

from __future__ import annotations

import importlib.util
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/99-closest-integer-audit")
EVIDENCE = Path("/audit-output/evidence")


def load_entry(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


def outcome(function, value: str):
    try:
        result = function(value)
        return {"kind": "return", "type": type(result).__name__, "value": result}
    except Exception as error:  # The exception class is observable for invalid input.
        return {"kind": "exception", "type": type(error).__name__}


def mathematical_outcome(value: str):
    """Exact decimal closest integer, with exact ties away from zero."""
    try:
        decimal_value = Decimal(value)
        if not decimal_value.is_finite():
            raise ValueError("non-finite")
        result = int(decimal_value.to_integral_value(rounding=ROUND_HALF_UP))
        return {"kind": "return", "type": "int", "value": result}
    except (InvalidOperation, ValueError, OverflowError):
        return {"kind": "exception", "type": "invalid-decimal"}


canonical = load_entry("trusted_canonical", SCRATCH / "trusted" / "canonical.py")
candidate = load_entry("generated_entry", SCRATCH / "candidate" / "solution.py")

inputs: list[str] = [
    # Documented examples and tie examples.
    "10", "15.3", "14.5", "-14.5",
    # Empty/invalid boundary and the candidate's sign-branch boundary.
    "", "0", "-0", "+0", "0.0", "-0.0", "+0.0",
    "5e-324", "-5e-324",
    # Nearest-integer and half boundaries.
    "0.49", "0.49999999999999994", "0.5", "0.5000000000000001",
    "-0.49", "-0.49999999999999994", "-0.5", "-0.5000000000000001",
    "1.49", "1.5", "1.51", "-1.49", "-1.5", "-1.51",
    "2.4999999999999996", "2.5000000000000001",
    "-2.4999999999999996", "-2.5000000000000001",
    # Alternate spellings accepted by Python's float conversion.
    "2.50", "-2.50", "2.5e0", "-2.5e0", " 2.5 ", " +2.5",
]

# Deterministic representative decimals around many integer/half boundaries.
for integer_part in range(-25, 26):
    sign = "-" if integer_part < 0 else ""
    magnitude = abs(integer_part)
    for fractional_digits in ("00", "01", "49", "50", "51", "99",
                              "499", "500", "501", "999"):
        inputs.append(f"{sign}{magnitude}.{fractional_digits}")
        inputs.append(f"{sign}{magnitude}.{fractional_digits}0")

# Deterministic representative exponent spellings.
for coefficient in (-15, -5, -1, 0, 1, 5, 15):
    for exponent in (-3, -1, 0, 1, 3):
        inputs.append(f"{coefficient}e{exponent}")

# Deduplicate without changing the documented ordering.
inputs = list(dict.fromkeys(inputs))
(EVIDENCE / "02_differential_inputs.json").write_text(
    json.dumps(inputs, indent=2) + "\n", encoding="utf-8"
)

records = []
canonical_mismatches = []
mathematical_mismatches = []
for value in inputs:
    canonical_result = outcome(canonical, value)
    candidate_result = outcome(candidate, value)
    mathematical_result = mathematical_outcome(value)
    record = {
        "input": value,
        "canonical": canonical_result,
        "candidate": candidate_result,
        "exact_decimal_contract": mathematical_result,
    }
    records.append(record)
    if canonical_result != candidate_result:
        canonical_mismatches.append(record)
    if (mathematical_result["kind"] != "exception"
            and candidate_result != mathematical_result):
        mathematical_mismatches.append(record)

(EVIDENCE / "02_differential_results.json").write_text(
    json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

print(f"input count: {len(inputs)}")
print(f"candidate/canonical mismatch count: {len(canonical_mismatches)}")
print(f"candidate/exact-decimal mismatch count: {len(mathematical_mismatches)}")
print("candidate/canonical mismatches:")
print(json.dumps(canonical_mismatches, indent=2, sort_keys=True))
print("candidate/exact-decimal mismatches:")
print(json.dumps(mathematical_mismatches, indent=2, sort_keys=True))

raise SystemExit(1 if canonical_mismatches or mathematical_mismatches else 0)
