#!/usr/bin/env python3
"""Independent finite witnesses for the source/K recurrence correspondence."""

from __future__ import annotations

import json


def operational(operations: list[int]) -> bool:
    balance = 0
    for operation in operations:
        balance += operation
        if balance < 0:
            return True
    return False


def below_zero_from(balance: int, operations: list[int]) -> bool:
    if not operations:
        return False
    head, *tail = operations
    updated = balance + head
    return True if updated < 0 else below_zero_from(updated, tail)


def mutated_non_strict(operations: list[int]) -> bool:
    balance = 0
    for operation in operations:
        balance += operation
        if balance <= 0:
            return True
    return False


def mutated_test_before_update(operations: list[int]) -> bool:
    balance = 0
    for operation in operations:
        if balance < 0:
            return True
        balance += operation
    return False


def mutated_final_balance_only(operations: list[int]) -> bool:
    return sum(operations) < 0


cases = [
    [],
    [1, 2, 3],
    [1, 2, -4, 5],
    [-1],
    [5, -5],
    [1, -2, 2],
    [2, -1, -1],
]
comparisons = [
    {
        "operations": operations,
        "operational": operational(operations),
        "recurrence": below_zero_from(0, operations),
        "equal": operational(operations) == below_zero_from(0, operations),
    }
    for operations in cases
]
counterfactuals = {
    "strict_zero_boundary": {
        "operations": [5, -5],
        "actual": operational([5, -5]),
        "mutated_leq": mutated_non_strict([5, -5]),
    },
    "update_before_test": {
        "operations": [-1],
        "actual": operational([-1]),
        "mutated_pre_update_test": mutated_test_before_update([-1]),
    },
    "prefix_not_final_only": {
        "operations": [1, -2, 2],
        "actual": operational([1, -2, 2]),
        "mutated_final_balance_only": mutated_final_balance_only([1, -2, 2]),
    },
}
print(
    json.dumps(
        {
            "comparisons": comparisons,
            "all_recurrence_comparisons_equal": all(
                comparison["equal"] for comparison in comparisons
            ),
            "counterfactuals": counterfactuals,
            "all_counterfactuals_discriminate": all(
                entry["actual"]
                != next(
                    value
                    for key, value in entry.items()
                    if key.startswith("mutated_")
                )
                for entry in counterfactuals.values()
            ),
            "scope": (
                "Finite witnesses only; the universal correspondence follows "
                "by induction on the list using the empty and cons cases."
            ),
        },
        indent=2,
        sort_keys=True,
    )
)
