import itertools

from solution import select_words


VOWELS = "aeiouAEIOU"


def oracle(s, n):
    words = s.split()
    return [
        word
        for word in words
        if sum(1 for ch in word if ch not in VOWELS) == n
    ]


PROMPT_CASES = [
    ("Mary had a little lamb", 4, ["little"]),
    ("Mary had a little lamb", 3, ["Mary", "lamb"]),
    ("simple white space", 2, []),
    ("Hello world", 4, ["world"]),
    ("Uncle sam", 3, ["Uncle"]),
    ("", 0, []),
]


def main():
    checks = 0
    for s, n, expected in PROMPT_CASES:
        actual = select_words(s, n)
        assert actual == expected
        assert actual == oracle(s, n)
        checks += 1

    alphabet = "aB "
    for length in range(7):
        for chars in itertools.product(alphabet, repeat=length):
            s = "".join(chars)
            for n in range(7):
                assert select_words(s, n) == oracle(s, n)
                checks += 1

    structured = [
        "  a  BB aB ",
        "AEIOU aeiou",
        "bcdfghjklmnpqrstvwxyz",
        "A B C D E",
        "Mary had a little lamb",
        "z " * 40,
    ]
    for s in structured:
        for n in range(12):
            assert select_words(s, n) == oracle(s, n)
            checks += 1

    print(f"differential checks: {checks}; mismatches: 0")


if __name__ == "__main__":
    main()
