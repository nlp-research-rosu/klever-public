#!/usr/bin/env python3
"""Independent exact-rational and Python-float observations for K smoke cases."""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


def load_candidate():
    path = Path("/tmp/audit-work/reconstruction/solution.py")
    spec = importlib.util.spec_from_file_location("scratch_solution_for_semantics", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def exact_mad(values: list[Fraction]) -> Fraction:
    mean = sum(values, Fraction(0, 1)) / len(values)
    return sum((abs(value - mean) for value in values), Fraction(0, 1)) / len(values)


candidate = load_candidate()
cases: list[tuple[str, list[Fraction]]] = [
    ("documented", [Fraction(1), Fraction(2), Fraction(3), Fraction(4)]),
    ("singleton", [Fraction(5)]),
    ("mixed-sign", [Fraction(-2), Fraction(0), Fraction(2)]),
    ("fractions", [Fraction(1, 2), Fraction(3, 2)]),
]

for label, values in cases:
    exact = exact_mad(values)
    floats = [float(value) for value in values]
    python_value = candidate(floats)
    print(
        json.dumps(
            {
                "label": label,
                "rational_inputs": [
                    {"numerator": value.numerator, "denominator": value.denominator}
                    for value in values
                ],
                "exact_mad": {
                    "numerator": exact.numerator,
                    "denominator": exact.denominator,
                },
                "python_float_hex": python_value.hex(),
            },
            sort_keys=True,
        )
    )

try:
    candidate([])
except Exception as error:
    empty: dict[str, Any] = {
        "kind": "exception",
        "type": type(error).__name__,
        "message": str(error),
    }
else:
    empty = {"kind": "returned"}
print(json.dumps({"label": "empty", "python": empty}, sort_keys=True))

print(
    json.dumps(
        {
            "label": "negative-denominator-witness",
            "semantic_terms": ["rat(1,-1)", "rat(1,1)"],
            "mathematical_values": [-1, 1],
            "expected_exact_mad": {"numerator": 1, "denominator": 1},
        },
        sort_keys=True,
    )
)

