#!/usr/bin/env python3
"""Finite adversarial support for the independent Stage 3 judgment.

This is deliberately independent of the frozen Python implementation and of
the K summary equations as executable artifacts.  It transcribes the visible
operational loop and the visible recurrence into separate functions.
"""

from __future__ import annotations

from itertools import product


def operational_loop(codes: tuple[int, ...]) -> bool:
    happy = True
    previous2 = -1
    previous1 = -1
    i = 0
    for code in codes:
        if i >= 2 and (
            code == previous1
            or code == previous2
            or previous1 == previous2
        ):
            happy = False
        previous2 = previous1
        previous1 = code
        i = i + 1
    return i >= 3 and happy


def contract(codes: tuple[int, ...]) -> bool:
    return len(codes) >= 3 and all(
        len({codes[index], codes[index + 1], codes[index + 2]}) == 3
        for index in range(len(codes) - 2)
    )


def scan_happy(
    remaining: tuple[int, ...], i: int, previous2: int, previous1: int
) -> bool:
    if not remaining:
        return True
    current, *tail = remaining
    rest = tuple(tail)
    if i < 2:
        return scan_happy(rest, i + 1, previous1, current)
    return (
        current != previous1
        and current != previous2
        and previous1 != previous2
        and scan_happy(rest, i + 1, previous1, current)
    )


def generated_summary(codes: tuple[int, ...]) -> bool:
    return len(codes) >= 3 and scan_happy(codes, 0, -1, -1)


def mutated_summary(codes: tuple[int, ...], mutation: str) -> bool:
    happy = True
    p2 = -1
    p1 = -1
    i = 0
    for current in codes:
        if mutation == "omit_current_previous1":
            bad = current == p2 or p1 == p2
        elif mutation == "omit_current_previous2":
            bad = current == p1 or p1 == p2
        elif mutation == "omit_previous_pair":
            bad = current == p1 or current == p2
        elif mutation == "delay_guard":
            bad = i > 2 and (current == p1 or current == p2 or p1 == p2)
        else:
            raise ValueError(mutation)
        if i >= 2 and mutation != "delay_guard" and bad:
            happy = False
        if mutation == "delay_guard" and bad:
            happy = False
        p2, p1, i = p1, current, i + 1
    return i >= 3 and happy


alphabet = (-1, 0, 1, 2)
total = 0
operational_mismatches: list[tuple[int, ...]] = []
summary_mismatches: list[tuple[int, ...]] = []
for length in range(8):
    for case in product(alphabet, repeat=length):
        total += 1
        if operational_loop(case) != contract(case):
            operational_mismatches.append(case)
        if generated_summary(case) != contract(case):
            summary_mismatches.append(case)

print(f"alphabet={alphabet}")
print("lengths=0..7")
print(f"cases={total}")
print(f"operational_vs_contract_mismatches={len(operational_mismatches)}")
print(f"summary_vs_contract_mismatches={len(summary_mismatches)}")
print(f"operational_mismatch_examples={operational_mismatches[:5]}")
print(f"summary_mismatch_examples={summary_mismatches[:5]}")

examples = (
    (),
    (1,),
    (1, 2),
    (1, 2, 3),
    (1, 1, 2),
    (1, 2, 1),
    (1, 2, 2),
    (1, 2, 3, 1),
    (1, 2, 3, 2),
    (-1, 0, 1),
)
for case in examples:
    print(
        f"example={case} operational={operational_loop(case)} "
        f"summary={generated_summary(case)} contract={contract(case)}"
    )

for mutation in (
    "omit_current_previous1",
    "omit_current_previous2",
    "omit_previous_pair",
    "delay_guard",
):
    witness = next(
        case
        for length in range(3, 6)
        for case in product((0, 1, 2), repeat=length)
        if mutated_summary(case, mutation) != contract(case)
    )
    print(
        f"mutation={mutation} witness={witness} "
        f"mutated={mutated_summary(witness, mutation)} "
        f"contract={contract(witness)}"
    )
