#!/usr/bin/env python3
from itertools import product


ORDINARY = set("aeiouAEIOU")


def frozen_program_result(text: str) -> int:
    count = 0
    last = ""
    for char in text:
        count += int(char in ORDINARY)
        last = char
    count += int(last == "y")
    count += int(last == "Y")
    return count


def vowels_tail_recurrence(text: str, last: str = "") -> int:
    if not text:
        return int(last == "y") + int(last == "Y")
    char, rest = text[0], text[1:]
    return int(char in ORDINARY) + vowels_tail_recurrence(rest, char)


alphabet = "aAyYb"
checked = 0
mismatches: list[tuple[str, int, int]] = []
for length in range(7):
    for chars in product(alphabet, repeat=length):
        text = "".join(chars)
        expected = frozen_program_result(text)
        actual = vowels_tail_recurrence(text)
        checked += 1
        if actual != expected:
            mismatches.append((text, expected, actual))

print(f"exhaustive alphabet={alphabet!r} lengths=0..6 cases={checked}")
print(f"mismatches={len(mismatches)}")


def counts_y_anywhere(text: str) -> int:
    return sum(char in ORDINARY | {"y", "Y"} for char in text)


def double_counts_final_y(text: str) -> int:
    return counts_y_anywhere(text) + int(bool(text) and text[-1] in "yY")


def ignores_uppercase(text: str) -> int:
    lower = set("aeiou")
    return sum(char in lower for char in text) + int(bool(text) and text[-1] == "y")


def constant_zero(_text: str) -> int:
    return 0


mutations = {
    "counts y/Y in nonfinal positions": (counts_y_anywhere, "yA"),
    "double-counts final y/Y": (double_counts_final_y, "y"),
    "ignores uppercase vowels/final Y": (ignores_uppercase, "ACEDY"),
    "constant zero": (constant_zero, "a"),
}
for label, (mutant, witness) in mutations.items():
    expected = frozen_program_result(witness)
    mutated = mutant(witness)
    print(
        f"counterfactual {label}: witness={witness!r} "
        f"frozen={expected} mutant={mutated} rejected={expected != mutated}"
    )

raise SystemExit(1 if mismatches else 0)
