from itertools import product
from math import prod

from solution import sum_product


checked = 0
mismatches = []

for length in range(6):
    for values in product(range(-3, 4), repeat=length):
        numbers = list(values)
        expected = (sum(numbers), prod(numbers))
        actual = sum_product(numbers)
        checked += 1
        if actual != expected:
            mismatches.append((numbers, expected, actual))

extra_cases = [
    [10**30, -(10**30), 7],
    [-(10**20), -(10**20)],
    [0, -(10**40), 10**40],
]

for numbers in extra_cases:
    expected = (sum(numbers), prod(numbers))
    actual = sum_product(numbers)
    checked += 1
    if actual != expected:
        mismatches.append((numbers, expected, actual))

print(f"checked={checked} mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(mismatch)
    raise SystemExit(1)
