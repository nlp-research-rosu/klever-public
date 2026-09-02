#!/usr/bin/env python3
"""Finite independent witnesses for the three definitional summaries."""

from __future__ import annotations

import itertools
import json
import math


def zero_residue_count(n: int) -> int:
    return (n + 1) // 3


def choose_three(x: int) -> int:
    return x * (x - 1) * (x - 2) // 6


def expected_triples(n: int) -> int:
    z = zero_residue_count(n)
    return choose_three(z) + choose_three(n - z)


def brute_force(n: int) -> int:
    values = [i * i - i + 1 for i in range(1, n + 1)]
    return sum(sum(triple) % 3 == 0 for triple in itertools.combinations(values, 3))


sample_ns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 29, 50, 80]
mismatches = [
    {"n": n, "summary": expected_triples(n), "brute_force": brute_force(n)}
    for n in range(1, 81)
    if expected_triples(n) != brute_force(n)
]

counterfactuals = {
    "zeroResidueCount := n // 3": {
        "n": 5,
        "correct_zero_count": zero_residue_count(5),
        "mutated_zero_count": 5 // 3,
        "correct_result": expected_triples(5),
        "mutated_result": choose_three(5 // 3) + choose_three(5 - 5 // 3),
    },
    "chooseThree := product // 5": {
        "x": 5,
        "correct_result": choose_three(5),
        "mutated_result": 5 * 4 * 3 // 5,
    },
    "expectedTriples := first summand only": {
        "n": 5,
        "correct_result": expected_triples(5),
        "mutated_result": choose_three(zero_residue_count(5)),
    },
}

print(
    json.dumps(
        {
            "semantic_derivation": {
                "index_residue_fact": "i^2 - i + 1 is 0 mod 3 exactly when i is 2 mod 3; otherwise it is 1 mod 3",
                "zero_residue_count_for_1_through_n": "floor((n + 1) / 3)",
                "valid_triple_residue_shapes": ["(0,0,0)", "(1,1,1)"],
                "result": "C(z,3) + C(n-z,3)",
            },
            "samples": [
                {
                    "n": n,
                    "zero_residue_count": zero_residue_count(n),
                    "summary": expected_triples(n),
                    "brute_force": brute_force(n),
                }
                for n in sample_ns
            ],
            "tested_positive_n_range": [1, 80],
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "counterfactuals": counterfactuals,
            "counterfactuals_are_observable": all(
                witness["correct_result"] != witness["mutated_result"]
                for witness in counterfactuals.values()
            ),
            "note": "Finite witnesses support relevance/body sensitivity; the classification judgment rests on source shape and operational semantics, not testing alone.",
        },
        indent=2,
        sort_keys=True,
    )
)
