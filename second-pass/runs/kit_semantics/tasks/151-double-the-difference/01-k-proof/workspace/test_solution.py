from itertools import product
from random import Random

from solution import double_the_difference


def independent_oracle(values):
    total = 0
    for value in values:
        if type(value) is int and value > 0:
            # Parity is checked without remainder, unlike the implementation.
            if (value // 2) * 2 != value:
                total = total + value ** 2
    return total


alphabet = (-7, -2, -1, 0, 1, 2, 3, 8, 1.5, -3.25)
cases = []
for length in range(5):
    cases.extend(product(alphabet, repeat=length))

rng = Random(20260729)
for _ in range(1000):
    length = rng.randrange(21)
    cases.append(tuple(rng.choice(alphabet) for _ in range(length)))

mismatches = []
for case in cases:
    expected = independent_oracle(case)
    actual = double_the_difference(list(case))
    if actual != expected:
        mismatches.append((case, expected, actual))

print(f"cases={len(cases)} mismatches={len(mismatches)}")
if mismatches:
    raise AssertionError(mismatches[:5])
