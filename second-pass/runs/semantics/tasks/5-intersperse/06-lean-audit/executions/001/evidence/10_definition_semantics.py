#!/usr/bin/env python3
"""Finite adversarial checks for the independently read K recurrences."""

from __future__ import annotations

import itertools


def source_intersperse(numbers: list[int], delimiter: int) -> list[int]:
    result: list[int] = []
    for number in numbers:
        if result:
            result.append(delimiter)
        result.append(number)
    return result


def k_intersperse_acc(
    accumulator: list[int], rest: list[int], delimiter: int
) -> list[int]:
    if not rest:
        return accumulator
    value, tail = rest[0], rest[1:]
    if not accumulator:
        return k_intersperse_acc([value], tail, delimiter)
    return k_intersperse_acc(
        accumulator + [delimiter] + [value], tail, delimiter
    )


def k_intersperse_vs(numbers: list[int], delimiter: int) -> list[int]:
    return k_intersperse_acc([], numbers, delimiter)


def k_last_number(old: int, rest: list[int]) -> int:
    if not rest:
        return old
    return k_last_number(rest[0], rest[1:])


values = [-1, 0, 2]
delimiters = [-2, 0, 3]
cases = 0
for length in range(6):
    for numbers_tuple in itertools.product(values, repeat=length):
        numbers = list(numbers_tuple)
        for delimiter in delimiters:
            expected = source_intersperse(numbers, delimiter)
            observed = k_intersperse_vs(numbers, delimiter)
            assert observed == expected, (numbers, delimiter, observed, expected)
            if numbers:
                assert k_last_number(99, numbers) == numbers[-1]
            else:
                assert k_last_number(99, numbers) == 99
            cases += 1

counterfactuals = {
    "constant_empty": lambda xs, d: [],
    "identity": lambda xs, d: list(xs),
    "omit_delimiter": lambda xs, d: list(xs),
    "delimiter_before_first": lambda xs, d: (
        [] if not xs else [d] + source_intersperse(xs, d)
    ),
}
witnesses = {
    "constant_empty": ([7], 4),
    "identity": ([1, 2], 4),
    "omit_delimiter": ([1, 2], 4),
    "delimiter_before_first": ([1], 4),
}
for name, mutation in counterfactuals.items():
    numbers, delimiter = witnesses[name]
    expected = source_intersperse(numbers, delimiter)
    mutated = mutation(numbers, delimiter)
    assert mutated != expected, (name, numbers, delimiter)
    print(
        f"REJECTED_MUTATION {name}: input={numbers}, delimiter={delimiter}, "
        f"expected={expected}, mutated={mutated}"
    )

print(f"PASS: recurrence/source agreement on {cases} exhaustive finite cases")
print(
    "NOTE: finite checks support sensitivity only; coverage, disjointness, "
    "and structural descent are justified separately from the K equations."
)
