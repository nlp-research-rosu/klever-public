#!/usr/bin/env python3
"""Finite adversarial check of the independently identified recurrence."""

from itertools import product


def source_program(numbers: tuple[int, ...]) -> tuple[int, ...]:
    result: list[int] = []
    iteration_snapshot = tuple(numbers)
    for number in iteration_snapshot:
        if numbers.count(number) == 1:
            result.append(number)
    return tuple(result)


def keep_singles_acc(
    accumulator: tuple[int, ...],
    remaining: tuple[int, ...],
    original: tuple[int, ...],
) -> tuple[int, ...]:
    if not remaining:
        return accumulator
    head, tail = remaining[0], remaining[1:]
    if original.count(head) == 1:
        return keep_singles_acc(accumulator + (head,), tail, original)
    return keep_singles_acc(accumulator, tail, original)


def wrong_moving_count(
    accumulator: tuple[int, ...],
    remaining: tuple[int, ...],
) -> tuple[int, ...]:
    if not remaining:
        return accumulator
    head, tail = remaining[0], remaining[1:]
    if remaining.count(head) == 1:
        return wrong_moving_count(accumulator + (head,), tail)
    return wrong_moving_count(accumulator, tail)


cases = []
for length in range(6):
    cases.extend(product((-1, 0, 1), repeat=length))

mismatches = [
    numbers
    for numbers in cases
    if source_program(numbers) != keep_singles_acc((), numbers, numbers)
]
print(f"exhaustive_cases={len(cases)}")
print(f"source_vs_keepSinglesAcc_mismatches={len(mismatches)}")
assert not mismatches

witnesses = [
    (),
    (1,),
    (1, 2, 3),
    (1, 2, 3, 2, 4),
    (1, 1, 1),
    (-1, 0, -1, 1),
]
for witness in witnesses:
    print(f"witness {witness} -> {source_program(witness)}")

moving_count_witness = (1, 2, 1)
print(
    "counterfactual moving-count",
    moving_count_witness,
    "source=",
    source_program(moving_count_witness),
    "mutant=",
    wrong_moving_count((), moving_count_witness),
)
assert wrong_moving_count((), moving_count_witness) != source_program(
    moving_count_witness
)

order_witness = (1, 2, 3)
prepend_mutant = tuple(reversed(source_program(order_witness)))
print(
    "counterfactual prepend",
    order_witness,
    "source=",
    source_program(order_witness),
    "mutant=",
    prepend_mutant,
)
assert prepend_mutant != source_program(order_witness)

constant_witness = (7,)
print(
    "counterfactual constant-empty",
    constant_witness,
    "source=",
    source_program(constant_witness),
    "mutant=()",
)
assert source_program(constant_witness) != ()
print("SEMANTIC RECURRENCE CHECK PASSED")
