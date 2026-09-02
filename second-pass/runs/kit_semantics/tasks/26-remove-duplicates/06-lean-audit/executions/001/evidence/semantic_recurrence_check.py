#!/usr/bin/env python3
"""Finite adversarial check of the rdAcc equations against an independent oracle."""

from __future__ import annotations

from collections import Counter
from itertools import product


def rd_acc(acc: tuple[int, ...], rest: tuple[int, ...], whole: tuple[int, ...]):
    if not rest:
        return acc
    head, tail = rest[0], rest[1:]
    if sum(1 for item in whole if item == head) == 1:
        return rd_acc(acc + (head,), tail, whole)
    return rd_acc(acc, tail, whole)


def independent_oracle(values: tuple[int, ...]) -> tuple[int, ...]:
    frequencies = Counter(values)
    return tuple(value for value in values if frequencies[value] == 1)


def keep_all_mutation(values: tuple[int, ...]) -> tuple[int, ...]:
    return values


def keep_repeated_mutation(values: tuple[int, ...]) -> tuple[int, ...]:
    frequencies = Counter(values)
    return tuple(value for value in values if frequencies[value] > 1)


cases = [
    tuple(values)
    for length in range(7)
    for values in product((-1, 0, 1), repeat=length)
]
cases.extend(
    [
        (1, 2, 3, 2, 4),
        (-5, 0, -5, 9),
        (2**63, -(2**63), 2**63, 7),
        (7, 8, 7, 9, 8, 10),
    ]
)

mismatches = []
for values in cases:
    recurrence = rd_acc((), values, values)
    oracle = independent_oracle(values)
    if recurrence != oracle:
        mismatches.append((values, recurrence, oracle))

mutation_witness = (1, 2, 1, 3)
print(f"case_count={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
print(f"sample={mutation_witness}")
print(f"rdAcc={rd_acc((), mutation_witness, mutation_witness)}")
print(f"keep_all_mutation={keep_all_mutation(mutation_witness)}")
print(f"keep_repeated_mutation={keep_repeated_mutation(mutation_witness)}")
print(
    "keep_all_discriminated="
    f"{keep_all_mutation(mutation_witness) != independent_oracle(mutation_witness)}"
)
print(
    "keep_repeated_discriminated="
    f"{keep_repeated_mutation(mutation_witness) != independent_oracle(mutation_witness)}"
)
if mismatches:
    raise SystemExit(1)
