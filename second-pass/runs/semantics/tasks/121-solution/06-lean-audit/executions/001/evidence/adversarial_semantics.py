#!/usr/bin/env python3

from __future__ import annotations

import itertools
import json


def source_contract(values: tuple[int, ...]) -> int:
    return sum(
        value
        for index, value in enumerate(values)
        if index % 2 == 0 and value % 2 == 1
    )


def odd_at_even_acc(
    values: tuple[int, ...], even: bool, accumulator: int
) -> int:
    if not values:
        return accumulator
    value, rest = values[0], values[1:]
    if even:
        return odd_at_even_acc(
            rest, False, accumulator + value * (value % 2)
        )
    return odd_at_even_acc(rest, True, accumulator)


def mutated_constant_projection(values: tuple[int, ...]) -> int:
    accumulator = 0
    even = True
    for value in values:
        if even:
            projection = 0
            accumulator += projection * (projection % 2)
        even = not even
    return accumulator


def main() -> None:
    domain = range(-3, 4)
    checked = 0
    for length in range(6):
        for values in itertools.product(domain, repeat=length):
            expected = source_contract(values)
            observed = odd_at_even_acc(values, True, 0)
            assert observed == expected, (values, expected, observed)
            checked += 1

    witnesses = {
        "mod_positive": {"input": [5, 2], "result": 5 % 2},
        "mod_negative_dividend": {"input": [-3, 2], "result": -3 % 2},
        "mod_negative_divisor": {"input": [-3, -2], "result": -3 % -2},
        "addition": {"input": [7, -3], "result": 7 + -3},
        "multiplication": {"input": [-3, 2], "result": -3 * 2},
        "prompt_example_1": {
            "input": [5, 8, 7, 1],
            "result": source_contract((5, 8, 7, 1)),
        },
        "prompt_example_2": {
            "input": [3, 3, 3, 3, 3],
            "result": source_contract((3, 3, 3, 3, 3)),
        },
        "prompt_example_3": {
            "input": [30, 13, 24, 321],
            "result": source_contract((30, 13, 24, 321)),
        },
        "negative_odd_even_position": {
            "input": [-3, 8, -5],
            "result": source_contract((-3, 8, -5)),
        },
        "empty_extension": {"input": [], "result": source_contract(())},
    }
    mutation_input = (5, 8, 7, 1)
    mutation_observed = mutated_constant_projection(mutation_input)
    mutation_expected = source_contract(mutation_input)
    assert mutation_observed != mutation_expected
    print(
        json.dumps(
            {
                "checked_sequences": checked,
                "domain": "all lengths 0..5 over values -3..3",
                "recurrence_mismatches": 0,
                "constant_projection_mutation": {
                    "input": list(mutation_input),
                    "expected": mutation_expected,
                    "mutated": mutation_observed,
                    "detected": True,
                },
                "witnesses": witnesses,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
