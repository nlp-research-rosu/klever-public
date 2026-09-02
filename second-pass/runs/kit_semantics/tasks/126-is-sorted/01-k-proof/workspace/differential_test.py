from collections import Counter
from itertools import product

from solution import is_sorted


def oracle(values):
    ascending = all(
        values[index] <= values[index + 1]
        for index in range(len(values) - 1)
    )
    multiplicities = Counter(values)
    at_most_two = all(count <= 2 for count in multiplicities.values())
    return ascending and at_most_two


checked = 0
mismatches = []

for length in range(8):
    for candidate in product(range(5), repeat=length):
        values = list(candidate)
        actual = is_sorted(values)
        expected = oracle(values)
        checked += 1
        if actual != expected:
            mismatches.append((values, actual, expected))

boundaries = [
    [],
    [0],
    [0, 0],
    [0, 0, 0],
    [10**30],
    [0, 10**30],
    [10**30, 0],
    list(range(100)),
    [7, 7] + list(range(8, 100)),
    [7, 7, 7] + list(range(8, 100)),
]

for values in boundaries:
    actual = is_sorted(values)
    expected = oracle(values)
    checked += 1
    if actual != expected:
        mismatches.append((values, actual, expected))

print(f"checked={checked} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
