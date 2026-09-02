from itertools import product

from solution import split_words


def oracle(txt):
    if any(char.isspace() for char in txt):
        return txt.split()
    if "," in txt:
        return txt.split(",")
    odd_letters = "bdfhjlnprtvxz"
    return sum(1 for char in txt if char in odd_letters)


alphabet = ["a", "b", "z", ",", " ", "\t", "\v", "é", "β"]
cases = [
    "",
    "Hello world!",
    "Hello,world!",
    "abcdef",
    ",",
    "a,,b",
    " \t ",
    "\v",
    "β,é",
]
for size in range(1, 4):
    cases.extend("".join(chars) for chars in product(alphabet, repeat=size))

mismatches = []
for text in cases:
    actual = split_words(text)
    expected = oracle(text)
    if actual != expected:
        mismatches.append((text, actual, expected))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(repr(mismatch))
    raise SystemExit(1)
