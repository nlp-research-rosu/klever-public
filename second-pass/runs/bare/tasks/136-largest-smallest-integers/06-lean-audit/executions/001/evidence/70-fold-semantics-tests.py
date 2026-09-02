#!/usr/bin/env python3
"""Finite adversarial checks of the independently read K fold equations."""

from __future__ import annotations

import itertools
import json


def k_neg_candidate(value: int, accumulator: int | None) -> int:
    if accumulator is None:
        return value
    return value if value > accumulator else accumulator


def k_neg_step(value: int, accumulator: int | None) -> int | None:
    return (
        k_neg_candidate(value, accumulator)
        if value < 0
        else accumulator
    )


def k_pos_candidate(value: int, accumulator: int | None) -> int:
    if accumulator is None:
        return value
    return value if value < accumulator else accumulator


def k_pos_step(value: int, accumulator: int | None) -> int | None:
    return (
        k_pos_candidate(value, accumulator)
        if value > 0
        else accumulator
    )


def k_folds(values: tuple[int, ...]) -> tuple[int | None, int | None]:
    negative: int | None = None
    positive: int | None = None
    for value in values:
        negative = k_neg_step(value, negative)
        positive = k_pos_step(value, positive)
    return negative, positive


def independent_oracle(
    values: tuple[int, ...],
) -> tuple[int | None, int | None]:
    negatives = [value for value in values if value < 0]
    positives = [value for value in values if value > 0]
    return (
        max(negatives) if negatives else None,
        min(positives) if positives else None,
    )


def main() -> None:
    alphabet = (-3, -1, 0, 1, 3)
    checked = 0
    mismatches: list[dict[str, object]] = []
    for length in range(6):
        for values in itertools.product(alphabet, repeat=length):
            checked += 1
            observed = k_folds(values)
            expected = independent_oracle(values)
            if observed != expected:
                mismatches.append(
                    {
                        "values": values,
                        "k_folds": observed,
                        "oracle": expected,
                    }
                )

    adversarial = {
        "empty": {
            "input": (),
            "result": k_folds(()),
        },
        "zero_is_ignored": {
            "input": (0,),
            "result": k_folds((0,)),
        },
        "largest_negative_is_closest_to_zero": {
            "input": (-3, -1, -2),
            "result": k_folds((-3, -1, -2)),
        },
        "smallest_positive_is_closest_to_zero": {
            "input": (3, 1, 2),
            "result": k_folds((3, 1, 2)),
        },
        "mixed_and_repeated": {
            "input": (-1, 3, -1, 1, 0, 1),
            "result": k_folds((-1, 3, -1, 1, 0, 1)),
        },
    }
    counterfactuals = {
        "constant_none_rejected_by": {
            "input": (-1, 1),
            "required_result": independent_oracle((-1, 1)),
            "constant_none_result": (None, None),
        },
        "first_negative_rejected_by": {
            "input": (-3, -1),
            "required_result": independent_oracle((-3, -1)),
            "first_negative_result": (-3, None),
        },
        "first_positive_rejected_by": {
            "input": (3, 1),
            "required_result": independent_oracle((3, 1)),
            "first_positive_result": (None, 3),
        },
        "zero_as_positive_rejected_by": {
            "input": (0,),
            "required_result": independent_oracle((0,)),
            "mutated_result": (None, 0),
        },
    }
    print(
        json.dumps(
            {
                "status": "PASS" if not mismatches else "FAIL",
                "scope": {
                    "alphabet": alphabet,
                    "lengths": [0, 1, 2, 3, 4, 5],
                    "case_count": checked,
                },
                "mismatch_count": len(mismatches),
                "mismatches": mismatches[:20],
                "adversarial_examples": adversarial,
                "counterfactual_mutations": counterfactuals,
                "note": (
                    "This is finite evidence supporting the direct inductive "
                    "reading of the recurrence equations; it is not used as "
                    "a substitute for that mathematical argument."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
