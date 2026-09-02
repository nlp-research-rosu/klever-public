#!/usr/bin/env python3
"""Independent finite checks of the two frozen summary definitions."""

from __future__ import annotations

import itertools
import json


def choose3(size: int) -> int:
    return size * (size - 1) * (size - 2) // 6


def frozen_summary(n: int) -> int:
    zero_residue_size = (n + 1) // 3
    one_residue_size = n - zero_residue_size
    return choose3(zero_residue_size) + choose3(one_residue_size)


def direct_prompt_oracle(n: int) -> int:
    values = [index * index - index + 1 for index in range(1, n + 1)]
    return sum(
        1
        for left, middle, right in itertools.combinations(values, 3)
        if (left + middle + right) % 3 == 0
    )


def mutated_wrong_class_size(n: int) -> int:
    zero_residue_size = n // 3
    return choose3(zero_residue_size) + choose3(n - zero_residue_size)


def mutated_omit_one_residue_class(n: int) -> int:
    return choose3((n + 1) // 3)


tested = list(range(1, 81))
mismatches = [
    {
        "n": n,
        "summary": frozen_summary(n),
        "oracle": direct_prompt_oracle(n),
    }
    for n in tested
    if frozen_summary(n) != direct_prompt_oracle(n)
]

wrong_size_witnesses = [
    n
    for n in tested
    if mutated_wrong_class_size(n) != direct_prompt_oracle(n)
]
omitted_class_witnesses = [
    n
    for n in tested
    if mutated_omit_one_residue_class(n) != direct_prompt_oracle(n)
]

print(
    json.dumps(
        {
            "tested_n": [tested[0], tested[-1]],
            "case_count": len(tested),
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "prompt_example": {
                "n": 5,
                "summary": frozen_summary(5),
                "oracle": direct_prompt_oracle(5),
            },
            "residue_derivation": {
                "possible_value_residues_mod_3": [0, 1],
                "divisible_three_term_residue_multisets": [
                    [0, 0, 0],
                    [1, 1, 1],
                ],
                "zero_residue_indices": "i congruent to 2 modulo 3",
                "zero_residue_class_size": "(n + 1) // 3",
            },
            "counterfactual_wrong_class_size": {
                "mutation": "replace (n + 1) // 3 with n // 3",
                "first_failure_n": wrong_size_witnesses[0],
                "failure_count": len(wrong_size_witnesses),
            },
            "counterfactual_omit_class": {
                "mutation": "omit choose3(n - ((n + 1) // 3))",
                "first_failure_n": omitted_class_witnesses[0],
                "failure_count": len(omitted_class_witnesses),
            },
        },
        indent=2,
        sort_keys=True,
    )
)
