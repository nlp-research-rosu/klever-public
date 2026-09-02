import itertools
import random

from solution import remove_vowels


DELETE_VOWELS = str.maketrans("", "", "aeiouAEIOU")


def oracle(text):
    return text.translate(DELETE_VOWELS)


prompt_cases = [
    "",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
]

alphabet = "aAeEiIoOuUbZ0 \n"
exhaustive_cases = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(20260725)
sample_alphabet = (
    "\x00\x7f"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789 \n\t"
    "éΩ中🙂"
)
random_cases = [
    "".join(rng.choice(sample_alphabet) for _ in range(rng.randrange(81)))
    for _ in range(1000)
]

cases = prompt_cases + exhaustive_cases + random_cases
mismatches = [
    (text, remove_vowels(text), oracle(text))
    for text in cases
    if remove_vowels(text) != oracle(text)
]

print(
    "differential checks="
    f"{len(cases)} exhaustive={len(exhaustive_cases)} "
    f"random={len(random_cases)} mismatches={len(mismatches)}"
)
if mismatches:
    raise AssertionError(mismatches[:5])
