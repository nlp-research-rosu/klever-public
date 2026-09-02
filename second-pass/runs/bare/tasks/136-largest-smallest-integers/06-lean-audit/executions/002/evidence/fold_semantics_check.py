#!/usr/bin/env python3
"""Independent finite sensitivity checks for the frozen extrema recurrences."""

from __future__ import annotations

import itertools
import json
from typing import Callable, Iterable


OptInt = int | None


def operational_source(values: Iterable[int]) -> tuple[OptInt, OptInt]:
    """Direct oracle for the frozen Python body under the generated semantics."""

    largest_negative: OptInt = None
    smallest_positive: OptInt = None
    for value in values:
        if value < 0:
            if largest_negative is None:
                largest_negative = value
            elif value > largest_negative:
                largest_negative = value
        if value > 0:
            if smallest_positive is None:
                smallest_positive = value
            elif value < smallest_positive:
                smallest_positive = value
    return largest_negative, smallest_positive


def neg_candidate(value: int, previous: OptInt) -> OptInt:
    if previous is None:
        return value
    return value if value > previous else previous


def pos_candidate(value: int, previous: OptInt) -> OptInt:
    if previous is None:
        return value
    return value if value < previous else previous


def fold_equations(values: Iterable[int]) -> tuple[OptInt, OptInt]:
    negative: OptInt = None
    positive: OptInt = None
    for value in values:
        negative = (
            neg_candidate(value, negative) if value < 0 else negative
        )
        positive = (
            pos_candidate(value, positive) if value > 0 else positive
        )
    return negative, positive


def wrong_negative_candidate(value: int, previous: OptInt) -> OptInt:
    if previous is None:
        return value
    return value if value < previous else previous


def wrong_positive_candidate(value: int, previous: OptInt) -> OptInt:
    if previous is None:
        return value
    return value if value > previous else previous


def mutated_folds(
    values: Iterable[int],
    negative_candidate: Callable[[int, OptInt], OptInt] = neg_candidate,
    positive_candidate: Callable[[int, OptInt], OptInt] = pos_candidate,
) -> tuple[OptInt, OptInt]:
    negative: OptInt = None
    positive: OptInt = None
    for value in values:
        if value < 0:
            negative = negative_candidate(value, negative)
        if value > 0:
            positive = positive_candidate(value, positive)
    return negative, positive


alphabet = (-2, -1, 0, 1, 2)
inputs = [
    values
    for length in range(6)
    for values in itertools.product(alphabet, repeat=length)
]
mismatches = [
    {
        "input": values,
        "operational": operational_source(values),
        "folds": fold_equations(values),
    }
    for values in inputs
    if operational_source(values) != fold_equations(values)
]

negative_mutation_failures = [
    {
        "input": values,
        "operational": operational_source(values),
        "mutated": mutated_folds(
            values, negative_candidate=wrong_negative_candidate
        ),
    }
    for values in inputs
    if operational_source(values)
    != mutated_folds(values, negative_candidate=wrong_negative_candidate)
]
positive_mutation_failures = [
    {
        "input": values,
        "operational": operational_source(values),
        "mutated": mutated_folds(
            values, positive_candidate=wrong_positive_candidate
        ),
    }
    for values in inputs
    if operational_source(values)
    != mutated_folds(values, positive_candidate=wrong_positive_candidate)
]

adversarial_examples = {
    "empty": [],
    "zero_only": [0, 0],
    "negative_order_and_duplicate": [-5, -2, -3, -2],
    "positive_order_and_duplicate": [5, 2, 3, 2],
    "mixed_with_zero": [0, -9, 4, -1, 2, -3, 0],
    "sign_boundary": [-1, 0, 1],
}
example_results = {
    name: {
        "input": values,
        "operational": operational_source(values),
        "folds": fold_equations(values),
    }
    for name, values in adversarial_examples.items()
}

result = {
    "alphabet": alphabet,
    "maximum_length": 5,
    "input_count": len(inputs),
    "oracle_vs_fold_mismatch_count": len(mismatches),
    "first_oracle_vs_fold_mismatch": mismatches[:1],
    "wrong_negative_extremum_mismatch_count": len(
        negative_mutation_failures
    ),
    "first_wrong_negative_extremum_mismatch": negative_mutation_failures[:1],
    "wrong_positive_extremum_mismatch_count": len(
        positive_mutation_failures
    ),
    "first_wrong_positive_extremum_mismatch": positive_mutation_failures[:1],
    "adversarial_examples": example_results,
}
if mismatches:
    raise SystemExit(json.dumps(result, indent=2, sort_keys=True))
if not negative_mutation_failures or not positive_mutation_failures:
    raise SystemExit(json.dumps(result, indent=2, sort_keys=True))
print(json.dumps(result, indent=2, sort_keys=True))
