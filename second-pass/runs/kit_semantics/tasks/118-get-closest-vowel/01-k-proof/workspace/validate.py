from itertools import product
from random import Random
from string import ascii_letters

from solution import get_closest_vowel


def oracle(word):
    vowels = "aeiouAEIOU"
    for i in range(len(word) - 2, 0, -1):
        if (word[i] in vowels
                and word[i - 1] not in vowels
                and word[i + 1] not in vowels):
            return word[i]
    return ""


def main():
    cases = [
        "yogurt",
        "FULL",
        "quick",
        "ab",
        "",
        "babeXid",
    ]

    alphabet = "abEYZ"
    for length in range(8):
        cases.extend("".join(chars) for chars in product(alphabet, repeat=length))

    rng = Random(20260725)
    for _ in range(5000):
        length = rng.randrange(0, 41)
        cases.append("".join(rng.choice(ascii_letters) for _ in range(length)))

    mismatches = []
    for word in cases:
        actual = get_closest_vowel(word)
        expected = oracle(word)
        if actual != expected:
            mismatches.append((word, actual, expected))

    print(f"differential cases={len(cases)} mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print(repr(mismatch))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
