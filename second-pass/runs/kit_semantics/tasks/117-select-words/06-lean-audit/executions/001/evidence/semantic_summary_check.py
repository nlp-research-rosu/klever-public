#!/usr/bin/env python3
"""Finite adversarial check of the K summaries against direct loop behavior."""

from __future__ import annotations

from itertools import product


VOWELS = "aeiouAEIOU"


def direct_loop(s, n, word, count, accumulator, old_character):
    output = list(accumulator)
    character = old_character
    for character in s:
        if character == " ":
            if count == n and word != "":
                output.append(word)
            word = ""
            count = 0
        else:
            word = word + character
            if character not in VOWELS:
                count = count + 1
    return output, word, count, character


def flush_selected(accumulator, word, count, n):
    output = list(accumulator)
    if count == n and word != "":
        output.append(word)
    return output


def scan_accum(s, n, word, count, accumulator):
    output = list(accumulator)
    for character in s:
        if character == " ":
            if count == n and word != "":
                output.append(word)
            word = ""
            count = 0
        else:
            word += character
            if character not in VOWELS:
                count += 1
    return output


def word_after(s, word):
    for character in s:
        word = "" if character == " " else word + character
    return word


def count_after(s, count):
    for character in s:
        if character == " ":
            count = 0
        elif character not in VOWELS:
            count += 1
    return count


def char_after(s, old_character):
    return old_character if not s else s[-1]


def select_scan(s, n, word, count, accumulator):
    return flush_selected(
        scan_accum(s, n, word, count, accumulator),
        word_after(s, word),
        count_after(s, count),
        n,
    )


checks = 0
alphabet = " aBé"
for length in range(6):
    for characters in product(alphabet, repeat=length):
        s = "".join(characters)
        for n in range(5):
            for word in ("", "z"):
                for count in (0, 2):
                    for accumulator in ((), ("seed",)):
                        for old_character in ("", "q"):
                            direct = direct_loop(
                                s, n, word, count, accumulator, old_character
                            )
                            summarized = (
                                scan_accum(s, n, word, count, accumulator),
                                word_after(s, word),
                                count_after(s, count),
                                char_after(s, old_character),
                            )
                            if direct != summarized:
                                raise AssertionError((s, n, direct, summarized))
                            expected_final = flush_selected(
                                direct[0], direct[1], direct[2], n
                            )
                            observed_final = select_scan(
                                s, n, word, count, accumulator
                            )
                            if expected_final != observed_final:
                                raise AssertionError(
                                    (s, n, expected_final, observed_final)
                                )
                            checks += 1


def source_from_initial(s, n):
    output, word, count, _character = direct_loop(s, n, "", 0, (), "")
    return flush_selected(output, word, count, n)


def mutant_increment_vowels(s, n):
    words = []
    word = ""
    count = 0
    for character in s:
        if character == " ":
            if count == n and word:
                words.append(word)
            word = ""
            count = 0
        else:
            word += character
            if character in VOWELS:
                count += 1
    return flush_selected(words, word, count, n)


def mutant_emit_empty(s, n):
    words = []
    word = ""
    count = 0
    for character in s:
        if character == " ":
            if count == n:
                words.append(word)
            word = ""
            count = 0
        else:
            word += character
            if character not in VOWELS:
                count += 1
    if count == n:
        words.append(word)
    return words


def mutant_drop_final_flush(s, n):
    return direct_loop(s, n, "", 0, (), "")[0]


def mutant_no_count_reset(s, n):
    words = []
    word = ""
    count = 0
    for character in s:
        if character == " ":
            if count == n and word:
                words.append(word)
            word = ""
        else:
            word += character
            if character not in VOWELS:
                count += 1
    return flush_selected(words, word, count, n)


counterfactuals = [
    ("increment-vowels", "a", 0, mutant_increment_vowels),
    ("emit-empty", " ", 0, mutant_emit_empty),
    ("drop-final-flush", "b", 1, mutant_drop_final_flush),
    ("no-count-reset", "b a", 1, mutant_no_count_reset),
]
for name, s, n, mutant in counterfactuals:
    expected = source_from_initial(s, n)
    changed = mutant(s, n)
    if expected == changed:
        raise AssertionError((name, s, n, expected, changed))
    print(
        f"counterfactual={name} witness={s!r},{n} "
        f"source={expected!r} mutant={changed!r}"
    )

print(f"adversarial_state_checks={checks}")
print("mismatches=0")
