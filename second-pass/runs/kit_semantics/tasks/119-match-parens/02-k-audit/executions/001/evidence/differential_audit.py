#!/usr/bin/env python3
"""Reviewer-authored differential test for HumanEval 119."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path


def import_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


canonical = import_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = import_entry(
    "scratch_generated", Path("/tmp/audit-work/119-match-parens/solution.py")
)

named_cases = [
    ("prompt_yes", ["()(", ")"]),
    ("prompt_no", [")", ")"]),
    ("both_empty", ["", ""]),
    ("first_order_only", ["(", ")"]),
    ("second_order_only", [")", "("]),
    ("both_orders_good", ["()", "(())"]),
    ("positive_final_balance", ["(", "("]),
    ("negative_final_balance", [")", ")"]),
    ("zero_balance_bad_prefix_both_orders", [")(", ")("]),
    ("empty_left_boundary", ["", "()"]),
    ("empty_right_boundary", ["()", ""]),
    ("deep_prefix", ["(((", ")))"]),
]

for label, pair in named_cases:
    expected = canonical(list(pair))
    actual = generated(list(pair))
    assert actual == expected, (label, pair, expected, actual)
    print(f"named {label}: {pair!r} -> {actual}")


def paren_strings(length: int):
    for characters in itertools.product("()", repeat=length):
        yield "".join(characters)


checked = 0
outcome_counts = {"Yes": 0, "No": 0}
for total_length in range(11):
    for left_length in range(total_length + 1):
        right_length = total_length - left_length
        for left in paren_strings(left_length):
            for right in paren_strings(right_length):
                pair = [left, right]
                expected = canonical(pair)
                actual = generated(pair)
                assert actual == expected, (pair, expected, actual)
                outcome_counts[actual] += 1
                checked += 1

print(
    f"exhaustive combined_length<=10: {checked} pairs, "
    f"Yes={outcome_counts['Yes']}, No={outcome_counts['No']}, mismatches=0"
)
print("DIFFERENTIAL CHECK: PASS")
