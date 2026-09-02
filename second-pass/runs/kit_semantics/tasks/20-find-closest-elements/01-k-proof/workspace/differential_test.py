from itertools import combinations
import random

from solution import find_closest_elements


def check_case(numbers):
    result = find_closest_elements(numbers)
    pairs = list(combinations(numbers, 2))
    best_distance = min(abs(right - left) for left, right in pairs)
    represented = any(
        result == (min(left, right), max(left, right))
        for left, right in pairs
    )
    return (
        isinstance(result, tuple)
        and len(result) == 2
        and result[0] <= result[1]
        and represented
        and abs(result[1] - result[0]) == best_distance
    )


cases = [
    [1.0, 2.0],
    [2.0, 1.0],
    [3.0, 3.0],
    [-10.0, -3.0, -3.25, 20.0],
    [1.0, 2.0, 3.0, 4.0, 5.0, 2.2],
    [1.0, 2.0, 3.0, 4.0, 5.0, 2.0],
]

rng = random.Random(20260724)
for _ in range(1000):
    length = rng.randint(2, 8)
    cases.append([round(rng.uniform(-1000.0, 1000.0), 3) for _ in range(length)])

failures = [numbers for numbers in cases if not check_case(numbers)]
print(f"cases={len(cases)} mismatches={len(failures)}")
if failures:
    raise AssertionError(failures[:3])
