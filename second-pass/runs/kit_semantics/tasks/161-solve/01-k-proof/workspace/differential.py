"""Independent finite oracle checks for solution.solve."""

from itertools import product
from random import Random

from solution import solve


def oracle(s):
    if any(ch.isalpha() for ch in s):
        return "".join(ch.swapcase() if ch.isalpha() else ch for ch in s)
    return s[::-1]


def main():
    checked = 0
    mismatches = []

    # Exhaustive ASCII strings of length zero, one, and two.
    alphabet = [chr(i) for i in range(128)]
    for length in range(3):
        for chars in product(alphabet, repeat=length):
            source = "".join(chars)
            checked += 1
            actual = solve(source)
            expected = oracle(source)
            if actual != expected:
                mismatches.append((source, actual, expected))

    # Seeded broader sample, including non-ASCII alphabetic and uncased letters.
    rng = Random(20260730)
    unicode_alphabet = (
        alphabet
        + list("éÉßΩωЖж中١Ⅰⅰͅ")
        + ["\N{LATIN SMALL LETTER DOTLESS I}", "\N{GREEK SMALL LETTER FINAL SIGMA}"]
    )
    for _ in range(5000):
        source = "".join(
            rng.choice(unicode_alphabet) for _ in range(rng.randrange(0, 21))
        )
        checked += 1
        actual = solve(source)
        expected = oracle(source)
        if actual != expected:
            mismatches.append((source, actual, expected))

    edge_cases = [
        "aⅠ",  # U+2160 swapcases but is not alphabetic: keep it unchanged.
        "aͅ",  # U+0345 has a case mapping but is not alphabetic.
        "中1",  # An uncased alphabetic character prevents reversal.
        "Ⅰ1",  # No alphabetic character: reverse the whole string.
    ]
    for source in edge_cases:
        checked += 1
        actual = solve(source)
        expected = oracle(source)
        if actual != expected:
            mismatches.append((source, actual, expected))

    print(f"checked={checked} mismatches={len(mismatches)}")
    if mismatches:
        raise AssertionError(mismatches[:5])


if __name__ == "__main__":
    main()
