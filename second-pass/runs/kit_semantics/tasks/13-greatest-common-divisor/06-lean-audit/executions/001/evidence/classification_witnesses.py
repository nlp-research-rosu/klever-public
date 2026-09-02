#!/usr/bin/env python3
"""Finite adversarial witnesses for the independently read Euclidean equations."""

from __future__ import annotations

import json
import math


def summary(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)


def operational_loop(a: int, b: int) -> int:
    remainder = 0
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return abs(a)


adversarial = [
    (0, 0),
    (0, 7),
    (7, 0),
    (-7, 0),
    (6, 9),
    (-6, 9),
    (6, -9),
    (-6, -9),
    (25, 15),
    (3, 5),
    (1071, 462),
]

grid_mismatches: list[dict[str, int]] = []
step_mismatches: list[dict[str, int]] = []
for a in range(-25, 26):
    for b in range(-25, 26):
        observed = operational_loop(a, b)
        expected = math.gcd(a, b)
        if observed != summary(a, b) or observed != expected:
            grid_mismatches.append(
                {
                    "a": a,
                    "b": b,
                    "operational": observed,
                    "summary": summary(a, b),
                    "math_gcd": expected,
                }
            )
        if b != 0 and summary(a, b) != summary(b, a % b):
            step_mismatches.append({"a": a, "b": b})

result = {
    "adversarial_results": [
        {
            "a": a,
            "b": b,
            "python_mod": None if b == 0 else a % b,
            "operational_loop": operational_loop(a, b),
            "summary": summary(a, b),
            "math_gcd": math.gcd(a, b),
        }
        for a, b in adversarial
    ],
    "exhaustive_grid": {
        "a_range": [-25, 25],
        "b_range": [-25, 25],
        "case_count": 51 * 51,
        "operational_summary_oracle_mismatches": grid_mismatches,
        "guarded_recurrence_step_mismatches": step_mismatches,
    },
    "counterfactual_failures": {
        "constant_zero_at_6_9": {
            "mutated": 0,
            "required": summary(6, 9),
        },
        "identity_a_at_6_9": {
            "mutated": 6,
            "required": summary(6, 9),
        },
        "base_without_abs_at_minus_7_0": {
            "mutated": -7,
            "required": summary(-7, 0),
        },
        "recurrence_plus_one_at_6_4": {
            "mutated_next_summary": summary(4, (6 % 4) + 1),
            "required": summary(6, 4),
        },
    },
    "all_witness_checks_pass": (
        not grid_mismatches
        and not step_mismatches
        and summary(6, 9) != 0
        and summary(6, 9) != 6
        and summary(-7, 0) != -7
        and summary(4, (6 % 4) + 1) != summary(6, 4)
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
if not result["all_witness_checks_pass"]:
    raise SystemExit(1)
