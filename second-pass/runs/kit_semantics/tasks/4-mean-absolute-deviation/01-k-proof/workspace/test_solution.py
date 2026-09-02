import math
import random

from solution import mean_absolute_deviation


def oracle(numbers):
    if not numbers:
        return 0.0
    center = math.fsum(numbers) / len(numbers)
    return math.fsum(abs(number - center) for number in numbers) / len(numbers)


cases = [
    [],
    [1.0],
    [1.0, 2.0, 3.0, 4.0],
    [-1.0, 1.0],
    [-3.5, -0.5, 10.0],
    [1.0e-100, -1.0e-100, 3.0e-100],
    [1.0e100, 1.0e100, 1.0e100],
]

rng = random.Random(20260729)
for size in range(13):
    for _ in range(20):
        cases.append([rng.uniform(-1.0e6, 1.0e6) for _ in range(size)])

mismatches = []
for numbers in cases:
    actual = mean_absolute_deviation(numbers)
    expected = oracle(numbers)
    if not math.isclose(actual, expected, rel_tol=1.0e-12, abs_tol=1.0e-12):
        mismatches.append((numbers, actual, expected))

assert not mismatches, mismatches[:3]
print(f"differential-cases={len(cases)} mismatches={len(mismatches)}")
