#!/usr/bin/env python3

from __future__ import annotations


def scan_bad(accumulator: int, number: int) -> int:
    while number > 0:
        accumulator += int(number % 2 == 0)
        number = (number - number % 10) // 10
    return accumulator


def scan_number(number: int) -> int:
    return 0 if number > 0 else number


def append_candidate(accumulator: list[int], value: int) -> list[int]:
    return accumulator + [value] if scan_bad(0, value) == 0 else accumulator


def collect(accumulator: list[int], values: list[int]) -> list[int]:
    for value in values:
        accumulator = append_candidate(accumulator, value)
    return accumulator


def operational_iteration(values: list[int]) -> tuple[list[int], int, int, int]:
    result: list[int] = []
    value = 0
    number = 0
    bad = 0
    for value in values:
        number = value  # sum((value,)) in the supplied semantics
        bad = 0
        while number > 0:
            bad += int(number % 2 == 0)
            number //= 10
        if bad == 0:
            result.append(value)
    return result, value, number, bad


numbers = [-2468, -101, -10, -1, 0, 1, 2, 9, 10, 11, 15, 20, 33, 101, 1422, 2468, 99999]
for original in numbers:
    number = original
    bad = 0
    while number > 0:
        bad += int(number % 2 == 0)
        number //= 10
    assert scan_bad(0, original) == bad
    assert scan_number(original) == number
    print(f"PASS scan summaries n={original} bad={bad} final_number={number}")

lists = [
    [],
    [1],
    [2],
    [15, 33, 1422, 1],
    [152, 323, 1422, 10],
    [0, -1, -20, 11, 2468, 99999],
    [11, 11, 20, 33],
]
for values in lists:
    result, last_value, last_number, last_bad = operational_iteration(values)
    assert collect([], values) == result
    expected_value = values[-1] if values else 0
    expected_number = scan_number(values[-1]) if values else 0
    expected_bad = scan_bad(0, values[-1]) if values else 0
    assert (last_value, last_number, last_bad) == (
        expected_value,
        expected_number,
        expected_bad,
    )
    print(
        "PASS outer summaries "
        f"values={values} collected={result} "
        f"locals=({last_value},{last_number},{last_bad})"
    )

print("ALL_SUMMARY_SEMANTIC_CHECKS_PASS")
