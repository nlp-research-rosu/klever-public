#!/usr/bin/env python3
"""Finite witnesses accompanying the independent recurrence argument."""

from __future__ import annotations

import itertools


VOWELS = tuple(map(ord, "aeiouAEIOU"))


def operational_loop(codes: tuple[int, ...], accumulator: tuple[int, ...] = ()) -> tuple[int, ...]:
    result = accumulator
    for code in codes:
        if code not in VOWELS:
            result = result + (code,)
    return result


def remove_vowels_from(codes: tuple[int, ...], accumulator: tuple[int, ...]) -> tuple[int, ...]:
    if not codes:
        return accumulator
    head, tail = codes[0], codes[1:]
    if head in VOWELS:
        return remove_vowels_from(tail, accumulator)
    return remove_vowels_from(tail, accumulator + (head,))


def mutated_swapped_guard(codes: tuple[int, ...], accumulator: tuple[int, ...]) -> tuple[int, ...]:
    if not codes:
        return accumulator
    head, tail = codes[0], codes[1:]
    if head not in VOWELS:
        return mutated_swapped_guard(tail, accumulator)
    return mutated_swapped_guard(tail, accumulator + (head,))


def show(codes: tuple[int, ...]) -> None:
    observed = remove_vowels_from(codes, ())
    expected = operational_loop(codes)
    print(f"codes={codes} summary={observed} operational={expected} equal={observed == expected}")


def main() -> None:
    samples = (
        (),
        tuple(map(ord, "aeiouAEIOU")),
        tuple(map(ord, "bcdf")),
        tuple(map(ord, "Hello, World!")),
        tuple(map(ord, "AaEeXy")),
        (0, 97, 128512, 85, 33),
    )
    for sample in samples:
        show(sample)

    alphabet = (65, 69, 97, 101, 120, 33, 0, 128512)
    checked = 0
    mismatches = 0
    for length in range(5):
        for codes in itertools.product(alphabet, repeat=length):
            checked += 1
            if remove_vowels_from(codes, ()) != operational_loop(codes):
                mismatches += 1
    print(f"exhaustive_scope=alphabet^{0}..{4} cases={checked} mismatches={mismatches}")

    adversarial = {
        "constant_empty_on_consonant": (() == operational_loop((ord("b"),))),
        "identity_on_vowel": ((ord("a"),) == operational_loop((ord("a"),))),
        "swapped_guard_on_mixed": (
            mutated_swapped_guard(tuple(map(ord, "aBzE")), ())
            == operational_loop(tuple(map(ord, "aBzE")))
        ),
        "case_sensitive_vowel_A": ((ord("A"),) == operational_loop((ord("A"),))),
    }
    for name, mutation_survives in adversarial.items():
        print(f"mutation={name} survives={mutation_survives}")
    if mismatches or any(adversarial.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
