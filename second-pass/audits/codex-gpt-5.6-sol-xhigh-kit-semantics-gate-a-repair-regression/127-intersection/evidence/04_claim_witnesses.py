#!/usr/bin/env python3
"""Ground witnesses for both positive claim preconditions and postconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/127-intersection")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


canonical = load_entry("witness_canonical", ROOT / "trusted/canonical.py")
generated = load_entry("witness_solution", ROOT / "candidate-src/solution.py")


def no_divisors(number: int, start: int) -> bool:
    if start < 2:
        start = 2
    return all(number % divisor != 0 for divisor in range(start, number))


def prime_result(length: int) -> str:
    return "YES" if length >= 2 and no_divisors(length, 2) else "NO"


def run_loop_witness(number: int, divisor: int, flag: bool):
    initial = {"N": number, "I": divisor, "P": flag}
    precondition = divisor >= 2 and divisor <= number
    while divisor < number:
        if number % divisor == 0:
            flag = False
        divisor += 1
    expected_flag = initial["P"] and no_divisors(number, initial["I"])
    return {
        "state": initial,
        "precondition": precondition,
        "final_divisor": divisor,
        "actual_final_flag": flag,
        "claimed_final_flag": expected_flag,
        "claim_holds": divisor == number and flag == expected_flag,
    }


entry_cases = []
for first, second in [
    ((-3, -1), (-5, 5)),
    ((0, 4), (-2, 8)),
    ((8, 10), (-4, 3)),
]:
    a0, a1 = first
    b0, b1 = second
    formal_precondition = a0 <= a1 and b0 <= b1
    length = min(a1, b1) - max(a0, b0)
    claimed = prime_result(length)
    expected = canonical(first, second)
    actual = generated(first, second)
    entry_cases.append(
        {
            "interval1": first,
            "interval2": second,
            "formal_precondition": formal_precondition,
            "substituted_length": length,
            "primeResult": claimed,
            "canonical": expected,
            "generated": actual,
            "all_equal": claimed == expected == actual,
        }
    )

report = {
    "divisor_loop_witnesses": [
        run_loop_witness(5, 2, True),
        run_loop_witness(4, 2, True),
        run_loop_witness(6, 4, False),
    ],
    "intersection_entry_witnesses": entry_cases,
}
print(json.dumps(report, indent=2, sort_keys=True))

if not all(item["precondition"] and item["claim_holds"] for item in report["divisor_loop_witnesses"]):
    raise SystemExit(1)
if not all(item["formal_precondition"] and item["all_equal"] for item in entry_cases):
    raise SystemExit(1)
