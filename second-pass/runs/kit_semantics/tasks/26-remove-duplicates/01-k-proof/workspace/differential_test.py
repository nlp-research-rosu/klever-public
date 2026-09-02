from collections import Counter
from itertools import product
import random

from solution import remove_duplicates


def oracle(values):
    counts = Counter(values)
    return [value for value in values if counts[value] == 1]


checked = 0
mismatches = []

for length in range(7):
    for values in product(range(-2, 3), repeat=length):
        sample = list(values)
        actual = remove_duplicates(sample)
        expected = oracle(sample)
        checked += 1
        if actual != expected:
            mismatches.append((sample, actual, expected))

rng = random.Random(20260724)
for _ in range(2000):
    sample = [rng.randint(-100, 100) for _ in range(rng.randint(0, 40))]
    actual = remove_duplicates(sample)
    expected = oracle(sample)
    checked += 1
    if actual != expected:
        mismatches.append((sample, actual, expected))

print(f"differential cases: {checked}")
print(f"mismatches: {len(mismatches)}")
if mismatches:
    print(f"first mismatch: {mismatches[0]}")
    raise SystemExit(1)
