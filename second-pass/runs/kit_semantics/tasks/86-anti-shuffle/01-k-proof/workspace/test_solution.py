#!/usr/bin/env python3
"""Independent differential and intent checks for solution.anti_shuffle."""

import itertools
import random
import string

from solution import anti_shuffle


def oracle(value):
    return " ".join("".join(sorted(word)) for word in value.split(" "))


def check(value):
    actual = anti_shuffle(value)
    expected = oracle(value)
    if actual != expected:
        raise AssertionError((value, actual, expected))

    before = value.split(" ")
    after = actual.split(" ")
    if len(before) != len(after):
        raise AssertionError(("space structure", value, actual))
    for source_word, result_word in zip(before, after):
        if result_word != "".join(sorted(source_word)):
            raise AssertionError(("word order", source_word, result_word))


def main():
    cases = {
        "",
        "Hi",
        "hello",
        "Hello World!!!",
        " ",
        "  ",
        "  cba  a",
        "tabs\tstay\tinside",
        "éΩ a😀",
        "😀éΩ Ω😀é",
    }

    alphabet = " aB!z"
    for length in range(6):
        cases.update(map("".join, itertools.product(alphabet, repeat=length)))

    rng = random.Random(20260729)
    ascii_alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    unicode_alphabet = " aZéΩ中😀!"
    for _ in range(2000):
        alphabet_for_case = (
            unicode_alphabet if rng.randrange(5) == 0 else ascii_alphabet
        )
        cases.add(
            "".join(
                rng.choice(alphabet_for_case)
                for _ in range(rng.randrange(41))
            )
        )

    for value in cases:
        check(value)

    print(f"differential_cases={len(cases)} mismatches=0")


if __name__ == "__main__":
    main()
