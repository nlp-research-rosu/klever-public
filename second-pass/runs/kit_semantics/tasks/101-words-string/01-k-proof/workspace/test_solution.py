from itertools import product

from solution import words_string


def oracle(source):
    words = []
    current = []
    for character in source:
        if character == "," or character.isspace():
            if current:
                words.append("".join(current))
                current = []
        else:
            current.append(character)
    if current:
        words.append("".join(current))
    return words


explicit = [
    "Hi, my name is John",
    "One, two, three, four, five, six",
    "",
    ",",
    "  alpha,,\tbeta\n",
    "one\v\f\u00a0two",
]
alphabet = "aB0, \t\n"
cases = list(explicit)
for length in range(6):
    cases.extend("".join(chars) for chars in product(alphabet, repeat=length))

mismatches = []
for source in cases:
    expected = oracle(source)
    actual = words_string(source)
    if actual != expected:
        mismatches.append((source, expected, actual))

assert not mismatches, mismatches[:10]
print(f"CPYTHON_DIFFERENTIAL_OK cases={len(cases)} mismatches=0")
