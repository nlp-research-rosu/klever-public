#!/usr/bin/env python3
"""Finite adversarial checks of the pluck recurrence against an independent oracle."""

from __future__ import annotations

import itertools


def operational_loop(values: tuple[int, ...]) -> list[int]:
    best = -1
    best_index = -1
    index = 0
    for value in values:
        if value % 2 == 0:
            if best == -1:
                best = value
                best_index = index
            elif value < best:
                best = value
                best_index = index
        index += 1
    return [] if best == -1 else [best, best_index]


def declarative_oracle(values: tuple[int, ...]) -> list[int]:
    evens = [(value, index) for index, value in enumerate(values) if value % 2 == 0]
    if not evens:
        return []
    value, index = min(evens, key=lambda pair: (pair[0], pair[1]))
    return [value, index]


def k_summary_recurrence(values: tuple[int, ...]) -> list[int]:
    best = -1
    best_index = -1
    index = 0
    last = 0
    for value in values:
        old_best = best
        if value % 2 == 0 and old_best == -1:
            best = value
        elif value % 2 == 0 and old_best != -1 and value < old_best:
            best = value
        elif value % 2 != 0:
            best = old_best
        elif value % 2 == 0 and old_best != -1 and value >= old_best:
            best = old_best
        else:
            raise AssertionError("nextBest guards were not exhaustive")

        if value % 2 == 0 and old_best == -1:
            best_index = index
        elif value % 2 == 0 and old_best != -1 and value < old_best:
            best_index = index
        elif value % 2 != 0:
            best_index = best_index
        elif value % 2 == 0 and old_best != -1 and value >= old_best:
            best_index = best_index
        else:
            raise AssertionError("nextBestIndex guards were not exhaustive")
        index += 1
        last = value
    assert index == len(values)
    assert last == (values[-1] if values else 0)
    return [] if best == -1 else [best, best_index]


def mutated_later_tie(values: tuple[int, ...]) -> list[int]:
    evens = [(value, index) for index, value in enumerate(values) if value % 2 == 0]
    if not evens:
        return []
    best = min(value for value, _index in evens)
    return [best, max(index for value, index in evens if value == best)]


def main() -> None:
    checked = 0
    mismatches: list[tuple[tuple[int, ...], object, object, object]] = []
    for length in range(7):
        for values in itertools.product(range(6), repeat=length):
            operational = operational_loop(values)
            oracle = declarative_oracle(values)
            summary = k_summary_recurrence(values)
            checked += 1
            if not (operational == oracle == summary):
                mismatches.append((values, operational, oracle, summary))

    guard_failures = []
    for value in range(-6, 7):
        for best in range(-6, 7):
            guards = [
                value % 2 == 0 and best == -1,
                value % 2 == 0 and best != -1 and value < best,
                value % 2 != 0,
                value % 2 == 0 and best != -1 and value >= best,
            ]
            if sum(guards) != 1:
                guard_failures.append((value, best, guards))

    witnesses = {
        "constant_empty_rejected": {
            "input": [0],
            "expected": declarative_oracle((0,)),
            "mutant": [],
        },
        "identity_rejected": {
            "input": [3, 2],
            "expected": declarative_oracle((3, 2)),
            "mutant": [3, 2],
        },
        "hardcoded_index_zero_rejected": {
            "input": [3, 2],
            "expected": declarative_oracle((3, 2)),
            "mutant": [2, 0],
        },
        "later_tie_rejected": {
            "input": [0, 3, 0],
            "expected": declarative_oracle((0, 3, 0)),
            "mutant": mutated_later_tie((0, 3, 0)),
        },
        "odd_minimum_rejected": {
            "input": [1, 2],
            "expected": declarative_oracle((1, 2)),
            "mutant": [1, 0],
        },
    }
    print(f"exhaustive_nonnegative_lists_checked={checked}")
    print(f"recurrence_mismatch_count={len(mismatches)}")
    print(f"guard_partition_cases_checked={13 * 13}")
    print(f"guard_partition_failure_count={len(guard_failures)}")
    for name, witness in witnesses.items():
        print(
            f"{name}: input={witness['input']} expected={witness['expected']} "
            f"mutant={witness['mutant']} rejected="
            f"{witness['expected'] != witness['mutant']}"
        )


if __name__ == "__main__":
    main()
