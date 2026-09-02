#!/usr/bin/env python3
"""Independent executable checks of the Stage 1 summary recurrences."""

from __future__ import annotations

import random


PRIME_TUPLE = (
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
)


def mathematical_prime(n: int) -> bool:
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def direct_program(sentence: str) -> str:
    result = ""
    word = ""
    for char in sentence:
        if char == " ":
            if len(word) in PRIME_TUPLE:
                result = result + word + " "
            word = ""
        else:
            word = word + char
    if len(word) in PRIME_TUPLE:
        result = result + word + " "
    return result.strip()


def emit_word(word: str, output: str) -> str:
    return output + word + " " if len(word) in PRIME_TUPLE else output


def scan_output(remaining: str, word: str, output: str) -> str:
    for char in remaining:
        if char == " ":
            output = emit_word(word, output)
            word = ""
        else:
            word = word + char
    return output


def scan_word(remaining: str, word: str) -> str:
    for char in remaining:
        if char == " ":
            word = ""
        else:
            word = word + char
    return word


def scan_last(remaining: str, previous: str) -> str:
    for char in remaining:
        previous = char
    return previous


def sentence_result(sentence: str) -> str:
    return emit_word(
        scan_word(sentence, ""),
        scan_output(sentence, "", ""),
    ).strip()


def intended_oracle(sentence: str) -> str:
    return " ".join(
        word for word in sentence.split(" ")
        if mathematical_prime(len(word))
    )


def cases() -> list[str]:
    result = [
        "a", " ", "  ", "aa", "aa ", " aa", "a  bb   ccc",
        "This is a test", "lets go for swimming",
    ]
    result.extend("a" * length for length in range(1, 101))
    for left in range(1, 99):
        for right in range(1, 100 - left):
            result.append("a" * left + " " + "b" * right)
    rng = random.Random(14320260731)
    alphabet = "abc "
    for _ in range(5000):
        length = rng.randint(1, 100)
        result.append("".join(rng.choice(alphabet) for _ in range(length)))
    return result


def first_counterfactual_witnesses() -> dict[str, tuple[str, str, str]]:
    witnesses: dict[str, tuple[str, str, str]] = {}

    def mutated_separator(sentence: str) -> str:
        return direct_program(sentence).replace(" ", "x")

    def omit_final_emit(sentence: str) -> str:
        return scan_output(sentence, "", "").strip()

    def every_length_selected(sentence: str) -> str:
        return " ".join(sentence.split(" "))

    mutations = {
        "space_to_x": mutated_separator,
        "omit_final_emit": omit_final_emit,
        "select_every_length": every_length_selected,
    }
    for name, mutation in mutations.items():
        for sentence in cases():
            expected = direct_program(sentence)
            observed = mutation(sentence)
            if expected != observed:
                witnesses[name] = (sentence, expected, observed)
                break
    return witnesses


def main() -> None:
    tested = cases()
    recurrence_mismatches = [
        (sentence, direct_program(sentence), sentence_result(sentence))
        for sentence in tested
        if direct_program(sentence) != sentence_result(sentence)
    ]
    intent_mismatches = [
        (sentence, direct_program(sentence), intended_oracle(sentence))
        for sentence in tested
        if direct_program(sentence) != intended_oracle(sentence)
    ]
    prime_table_mismatches = [
        n for n in range(0, 101)
        if (n in PRIME_TUPLE) != mathematical_prime(n)
    ]
    last_mismatches = [
        sentence for sentence in tested
        if scan_last(sentence, "") != sentence[-1:]
    ]
    print(f"TESTED_SENTENCES={len(tested)}")
    print(f"RECURRENCE_MISMATCHES={len(recurrence_mismatches)}")
    print(f"INTENT_MISMATCHES={len(intent_mismatches)}")
    print(f"PRIME_TABLE_MISMATCHES_0_TO_100={prime_table_mismatches}")
    print(f"SCAN_LAST_MISMATCHES={len(last_mismatches)}")
    print(f"COUNTERFACTUAL_WITNESSES={first_counterfactual_witnesses()!r}")
    if recurrence_mismatches or intent_mismatches or prime_table_mismatches or last_mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
