#!/usr/bin/env python3
"""Finite adversarial evidence for the frozen #vowels recurrence."""

from __future__ import annotations

from itertools import product


ORDINARY = frozenset("aeiouAEIOU")
FINAL_Y = frozenset("yY")


def contract_oracle(text: str) -> int:
    ordinary = sum(character in ORDINARY for character in text)
    final_y = int(bool(text) and text[-1] in FINAL_Y)
    return ordinary + final_y


def frozen_recurrence(text: str) -> int:
    if text == "":
        return 0
    if text[0] in ORDINARY:
        return 1 + frozen_recurrence(text[1:])
    if len(text) == 1 and text[0] in FINAL_Y:
        return 1
    return frozen_recurrence(text[1:])


def mutation_y_everywhere(text: str) -> int:
    return sum(character in ORDINARY | FINAL_Y for character in text)


def mutation_no_final_y(text: str) -> int:
    return sum(character in ORDINARY for character in text)


alphabet = "aAeEyYbz"
tested = 0
mismatches: list[tuple[str, int, int]] = []
for length in range(7):
    for characters in product(alphabet, repeat=length):
        text = "".join(characters)
        expected = contract_oracle(text)
        actual = frozen_recurrence(text)
        tested += 1
        if actual != expected:
            mismatches.append((text, expected, actual))

witnesses = [
    "",
    "y",
    "Y",
    "yy",
    "yby",
    "ay",
    "ACEDY",
    "rhythm",
    "abcde",
    "bYb",
]
print(f"alphabet={alphabet!r}")
print("lengths=0..6")
print(f"tested={tested}")
print(f"mismatch_count={len(mismatches)}")
for text in witnesses:
    print(
        repr(text),
        f"contract={contract_oracle(text)}",
        f"recurrence={frozen_recurrence(text)}",
        f"y_everywhere_mutation={mutation_y_everywhere(text)}",
        f"no_final_y_mutation={mutation_no_final_y(text)}",
    )
