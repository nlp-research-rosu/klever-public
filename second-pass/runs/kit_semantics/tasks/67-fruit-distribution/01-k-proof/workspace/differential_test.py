import re

from solution import fruit_distribution


def oracle(text, total):
    match = re.fullmatch(r"([0-9]+) apples and ([0-9]+) oranges", text)
    if match is None:
        raise ValueError("outside the documented input format")
    apples, oranges = map(int, match.groups())
    return total - apples - oranges


examples = [
    ("5 apples and 6 oranges", 19),
    ("0 apples and 1 oranges", 3),
    ("2 apples and 3 oranges", 100),
    ("100 apples and 1 oranges", 120),
]
boundaries = [0, 1, 2, 9, 10, 11, 99, 100, 101, 999, 1000, 12345]
cases = list(examples)
for apples in boundaries:
    for oranges in boundaries:
        for mangoes in (0, 1, 37):
            cases.append(
                (f"{apples} apples and {oranges} oranges",
                 apples + oranges + mangoes)
            )

mismatches = []
for text, total in cases:
    actual = fruit_distribution(text, total)
    expected = oracle(text, total)
    if actual != expected:
        mismatches.append((text, total, actual, expected))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:5])
