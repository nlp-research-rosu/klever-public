from collections import Counter
from itertools import product

from solution import histogram


def oracle(text):
    counts = Counter(character for character in text if character != " ")
    if not counts:
        return {}
    maximum = max(counts.values())
    return {
        character: count
        for character, count in counts.items()
        if count == maximum
    }


alphabet = "abc "
cases = [
    "".join(characters)
    for length in range(8)
    for characters in product(alphabet, repeat=length)
]
cases.extend([
    "a b c",
    "a b b a",
    "a b c a b",
    "b b b b a",
    "",
])

mismatches = []
for case in cases:
    actual = histogram(case)
    expected = oracle(case)
    if actual != expected:
        mismatches.append((case, actual, expected))

print("cases:", len(cases))
print("mismatches:", len(mismatches))
if mismatches:
    print("first mismatch:", mismatches[0])
    raise SystemExit(1)
