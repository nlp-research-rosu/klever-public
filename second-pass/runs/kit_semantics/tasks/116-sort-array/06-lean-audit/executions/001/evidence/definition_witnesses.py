#!/usr/bin/env python3
"""Ground witnesses for the independently classified Stage 1 definitions."""

from __future__ import annotations

import json


def k_bin_codes(n: int) -> list[int]:
    assert n >= 0
    if n == 0:
        return [48]
    acc: list[int] = []
    while n > 0:
        digit = n % 2
        n = (n - digit) // 2
        acc.insert(0, 48 + digit)
    return acc


def k_cnt_sub(codes: list[int], pattern: list[int]) -> int:
    if not codes:
        return 0
    if pattern and codes[: len(pattern)] == pattern:
        return 1 + k_cnt_sub(codes[len(pattern) :], pattern)
    return k_cnt_sub(codes[1:], pattern)


def popcount_abs(n: int) -> int:
    magnitude = n if n >= 0 else 0 - n
    return k_cnt_sub(k_bin_codes(magnitude), [49])


def count_zero_mutation(n: int) -> int:
    magnitude = abs(n)
    return k_cnt_sub(k_bin_codes(magnitude), [48])


def source_sort(values: list[int]) -> list[int]:
    return sorted(sorted(values), key=lambda value: bin(value).count("1"))


def summary_sort(values: list[int]) -> list[int]:
    return sorted(sorted(values), key=popcount_abs)


integer_witnesses = [0, 1, 2, 5, 6, -1, -5, -6, 2**31 - 1, -(2**31)]
popcount_rows = [
    {
        "input": value,
        "k_summary": popcount_abs(value),
        "source_lambda": bin(value).count("1"),
        "equal": popcount_abs(value) == bin(value).count("1"),
    }
    for value in integer_witnesses
]

list_witnesses = [
    [],
    [1, 5, 2, 3, 4],
    [-2, -3, -4, -5, -6],
    [0, 1, 2, 3, 4],
    [7, -7, 0, 8, -1, 3, -4],
]
sort_rows = [
    {
        "input": values,
        "source": source_sort(values),
        "summary": summary_sort(values),
        "equal": source_sort(values) == summary_sort(values),
    }
    for values in list_witnesses
]

mutation_input = [1, 2, 3, 4]
mutation_source = source_sort(mutation_input)
mutation_output = sorted(sorted(mutation_input), key=count_zero_mutation)

report = {
    "allIntVS_boundary_reasoning": {
        "empty": True,
        "all_integer_sequence": True,
        "sequence_with_non_integer": False,
        "recurrence_descends_on_strict_tail": True,
    },
    "popcount_witnesses": popcount_rows,
    "sort_witnesses": sort_rows,
    "counterfactual_digit_49_to_48": {
        "input": mutation_input,
        "source_output": mutation_source,
        "mutated_output": mutation_output,
        "distinguished": mutation_source != mutation_output,
    },
    "counterfactual_negative_without_magnitude": {
        "input": -6,
        "binCodes_rule_applicable": False,
        "reason": "the frozen binCodes equations cover only 0 and positive integers",
    },
}
report["overall"] = (
    all(row["equal"] for row in popcount_rows)
    and all(row["equal"] for row in sort_rows)
    and report["counterfactual_digit_49_to_48"]["distinguished"]
    and not report["counterfactual_negative_without_magnitude"]["binCodes_rule_applicable"]
)
print(json.dumps(report, indent=2, sort_keys=True))
