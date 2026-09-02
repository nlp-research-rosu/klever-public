#!/usr/bin/env python3
"""Adversarial checks of the frozen loop summaries and counterfactuals."""

from __future__ import annotations

import json
from typing import Callable


def contribution(index: int, value: int) -> int:
    if index % 3 == 0:
        return value * value
    if index % 4 == 0:
        return value * value * value
    return value


def frozen_loop(
    values: list[int], index: int, total: int, old_value: int
) -> tuple[int, int, int]:
    value = old_value
    for value in values:
        if index % 3 == 0:
            total += value * value
        elif index % 4 == 0:
            total += value * value * value
        else:
            total += value
        index += 1
    return total, index, value


def recursive_summaries(
    values: list[int], index: int, total: int, old_value: int
) -> tuple[int, int, int]:
    if not values:
        return total, index, old_value
    head, *tail = values
    return recursive_summaries(
        tail,
        index + 1,
        total + contribution(index, head),
        head,
    )


cases = [
    ([], 0, 0, 91),
    ([2], 0, 0, -9),
    ([2, -3, 5, -7, 11], 0, 0, 0),
    (list(range(-6, 8)), 0, -17, 123),
    ([10, 20, 30, 40, 50], 2, 7, -1),
    ([3, -4, 5, -6, 7, -8], -4, 19, 42),
    ([0, 1, -1, 10**20, -(10**20)], 11, -(10**40), 5),
]

comparisons = []
for values, index, total, old_value in cases:
    operational = frozen_loop(values, index, total, old_value)
    summary = recursive_summaries(values, index, total, old_value)
    comparisons.append(
        {
            "values": values,
            "initial_index": index,
            "initial_total": total,
            "old_value": old_value,
            "operational": operational,
            "summary": summary,
            "match": operational == summary,
        }
    )


def sum_with(
    values: list[int],
    contribution_fn: Callable[[int, int], int],
) -> int:
    return sum(contribution_fn(index, value) for index, value in enumerate(values))


def cube_wins_overlap(index: int, value: int) -> int:
    if index % 4 == 0:
        return value**3
    if index % 3 == 0:
        return value**2
    return value


def constant_zero(_index: int, _value: int) -> int:
    return 0


def identity(_index: int, value: int) -> int:
    return value


mutation_witnesses = [
    {
        "mutation": "multiple-of-4 branch incorrectly precedes multiple-of-3",
        "values": [0] * 12 + [2],
        "expected": sum_with([0] * 12 + [2], contribution),
        "mutated": sum_with([0] * 12 + [2], cube_wins_overlap),
    },
    {
        "mutation": "contribution is constant zero",
        "values": [2, -3, 5],
        "expected": sum_with([2, -3, 5], contribution),
        "mutated": sum_with([2, -3, 5], constant_zero),
    },
    {
        "mutation": "contribution is identity",
        "values": [2],
        "expected": sum_with([2], contribution),
        "mutated": sum_with([2], identity),
    },
]
for witness in mutation_witnesses:
    witness["detected"] = witness["expected"] != witness["mutated"]

report = {
    "summary_comparisons": comparisons,
    "all_summary_comparisons_match": all(
        comparison["match"] for comparison in comparisons
    ),
    "counterfactual_mutations": mutation_witnesses,
    "all_counterfactual_mutations_detected": all(
        witness["detected"] for witness in mutation_witnesses
    ),
    "branch_partition": {
        "tested_indices": list(range(-24, 25)),
        "exactly_one_branch_each": all(
            sum(
                (
                    index % 3 == 0,
                    index % 3 != 0 and index % 4 == 0,
                    index % 3 != 0 and index % 4 != 0,
                )
            )
            == 1
            for index in range(-24, 25)
        ),
    },
}
report["status"] = (
    "PASS"
    if report["all_summary_comparisons_match"]
    and report["all_counterfactual_mutations_detected"]
    and report["branch_partition"]["exactly_one_branch_each"]
    else "FAIL"
)
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report["status"] == "PASS" else 1)
