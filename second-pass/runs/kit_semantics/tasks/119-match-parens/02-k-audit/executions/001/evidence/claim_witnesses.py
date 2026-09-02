#!/usr/bin/env python3
"""Ground substitutions for the SPEC.match-parens pre/postcondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def import_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


canonical = import_entry("canonical_witness", Path("/reference/canonical.py"))
generated = import_entry(
    "generated_witness", Path("/tmp/audit-work/119-match-parens/solution.py")
)


def paren_codes(codes):
    return all(code in {40, 41} for code in codes)


def good_parens(codes):
    balance = 0
    minimum = 0
    for code in codes:
        balance = balance + 1 if code == 40 else balance - 1
        minimum = min(balance, minimum)
    return balance == 0 and minimum >= 0


def match_answer(left_codes, right_codes):
    possible = good_parens(left_codes + right_codes) or good_parens(
        right_codes + left_codes
    )
    return "Yes" if possible else "No"


witnesses = [
    ("empty_satisfying_state", "", ""),
    ("only_second_order_good", ")", "("),
    ("both_orders_bad", ")", ")"),
]

for label, left, right in witnesses:
    left_codes = tuple(map(ord, left))
    right_codes = tuple(map(ord, right))
    precondition = paren_codes(left_codes) and paren_codes(right_codes)
    claimed = match_answer(left_codes, right_codes)
    canonical_result = canonical([left, right])
    generated_result = generated([left, right])
    assert precondition
    assert claimed == canonical_result == generated_result
    print(
        f"{label}: A={left_codes}, B={right_codes}, precondition=true, "
        f"matchAnswer={claimed}, canonical={canonical_result}, generated={generated_result}"
    )

print("GROUND CLAIM WITNESSES: PASS")
