#!/usr/bin/env python3
"""Finite adversarial cross-check of the frozen loop and summary recurrence."""

from __future__ import annotations

import itertools
import json


def operational(operations: tuple[int, ...]) -> bool:
    balance = 0
    for operation in operations:
        balance += operation
        if balance < 0:
            return True
    return False


def below_zero_from(balance: int, operations: tuple[int, ...]) -> bool:
    if not operations:
        return False
    head, *tail = operations
    updated = balance + head
    if updated < 0:
        return True
    return below_zero_from(updated, tuple(tail))


cases = [
    values
    for length in range(6)
    for values in itertools.product(range(-3, 4), repeat=length)
]
mismatches = [
    {
        "operations": values,
        "operational": operational(values),
        "recurrence": below_zero_from(0, values),
    }
    for values in cases
    if operational(values) != below_zero_from(0, values)
]

mutation_witnesses = {
    "constant_false": {
        "operations": [-1],
        "expected": operational((-1,)),
        "mutated": False,
    },
    "constant_true": {
        "operations": [],
        "expected": operational(()),
        "mutated": True,
    },
    "final_balance_only": {
        "operations": [-1, 2],
        "expected": operational((-1, 2)),
        "mutated": sum((-1, 2)) < 0,
    },
    "non_strict_boundary": {
        "operations": [5, -5],
        "expected": operational((5, -5)),
        "mutated": True,
    },
    "ignore_head": {
        "operations": [-1, 2],
        "expected": operational((-1, 2)),
        "mutated": operational((2,)),
    },
}

print(
    json.dumps(
        {
            "command": (
                "python3 "
                "/audit-output/evidence/05_semantic_crosscheck_command.py"
            ),
            "domain": {
                "lengths": "0..5",
                "element_values": "-3..3",
                "case_count": len(cases),
            },
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "counterfactual_mutation_witnesses": mutation_witnesses,
        },
        indent=2,
        sort_keys=True,
    )
)
