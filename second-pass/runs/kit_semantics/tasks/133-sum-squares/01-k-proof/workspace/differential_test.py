from fractions import Fraction
import random

from solution import sum_squares


def independent_ceil(value):
    fraction = Fraction(value)
    return -(-fraction.numerator // fraction.denominator)


def oracle(values):
    total = 0
    for value in values:
        rounded = independent_ceil(value)
        total += rounded * rounded
    return total


cases = [
    [],
    [1, 2, 3],
    [1, 4, 9],
    [1, 3, 5, 7],
    [1.4, 4.2, 0],
    [-2.4, 1, 1],
    [-3.0, -2.0000000000000004, -2.0, -1.9999999999999998],
    [0.0, -0.0, 0.0000000000000001, -0.0000000000000001],
]

rng = random.Random(20260725)
pool = [rng.randint(-10000, 10000) / 100.0 for _ in range(400)]
for _ in range(1000):
    length = rng.randint(0, 20)
    cases.append([rng.choice(pool) for _ in range(length)])

mismatches = []
for values in cases:
    actual = sum_squares(values)
    expected = oracle(values)
    if actual != expected:
        mismatches.append((values, actual, expected))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:5])
