from itertools import product
from random import Random

from solution import pluck


def oracle(arr):
    candidates = [(value, index) for index, value in enumerate(arr)
                  if value % 2 == 0]
    if not candidates:
        return []
    value, index = min(candidates)
    return [value, index]


checked = 0

for length in range(7):
    for values in product(range(6), repeat=length):
        arr = list(values)
        assert pluck(arr) == oracle(arr), arr
        checked += 1

rng = Random(20260729)
for _ in range(500):
    length = rng.randrange(0, 201)
    arr = [rng.randrange(0, 10001) for _ in range(length)]
    assert pluck(arr) == oracle(arr), arr
    checked += 1

for arr in (
    [1] * 10000,
    [2] * 10000,
    list(range(10000)),
    list(reversed(range(10000))),
):
    assert pluck(arr) == oracle(arr)
    checked += 1

print(f"differential-tests: {checked} cases, 0 mismatches")
