#!/usr/bin/env python3
"""Concrete witnesses for the exact-Rat versus Python-float semantics gap."""

from __future__ import annotations

import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path


def load(path: str, name: str):
    file_path = Path(path)
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


candidate = load("/tmp/audit-work/source/solution.py", "audit_candidate_gap")
canonical = load("/reference/canonical.py", "audit_canonical_gap")

power_53 = 2**53
rounding_input = [float(-power_53), 1.0, float(power_53)]
rounding_exact = [
    Fraction(0),
    Fraction(power_53 + 1, 2 * power_53),
    Fraction(1),
]

power_1023 = float(2**1023)
overflow_input = [-power_1023, 0.0, power_1023]


def encode_float(value: float):
    return {
        "repr": repr(value),
        "hex": value.hex(),
        "is_nan": math.isnan(value),
        "is_infinite": math.isinf(value),
    }


def run(function, values):
    return [encode_float(value) for value in function(list(values))]


record = {
    "rounding_witness": {
        "input": [encode_float(value) for value in rounding_input],
        "all_inputs_exactly_representable": True,
        "claim_c4_precondition": "-2^53 < 1 < 2^53",
        "K_exact_rational_postcondition": [str(value) for value in rounding_exact],
        "K_middle_equals_one_half": rounding_exact[1] == Fraction(1, 2),
        "candidate_python": run(candidate, rounding_input),
        "canonical_python": run(canonical, rounding_input),
        "false_conclusion": (
            "K claims the middle is (2^53+1)/2^54, while both Python "
            "implementations return exactly 1/2 after rounded subtraction."
        ),
    },
    "overflow_witness": {
        "input": [encode_float(value) for value in overflow_input],
        "all_inputs_finite_and_exactly_representable": True,
        "exact_rational_result": ["0", "1/2", "1"],
        "candidate_python": run(candidate, overflow_input),
        "canonical_python": run(canonical, overflow_input),
        "false_conclusion": (
            "Exact rationals put the maximum at 1, while Python's finite "
            "subtraction overflows and the maximum maps to NaN."
        ),
    },
}

print(json.dumps(record, indent=2, sort_keys=True))
