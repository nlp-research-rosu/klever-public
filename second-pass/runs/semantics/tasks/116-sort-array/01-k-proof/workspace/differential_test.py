from itertools import product
from random import Random

from solution import sort_array


def oracle(values):
    return sorted(values, key=lambda value: (bin(value).count("1"), value))


checked = 0
for length in range(5):
    for values in product(range(8), repeat=length):
        values = list(values)
        assert sort_array(values) == oracle(values)
        checked += 1

rng = Random(116)
for _ in range(500):
    values = [rng.randrange(0, 1_000_000) for _ in range(rng.randrange(0, 60))]
    assert sort_array(values) == oracle(values)
    checked += 1

print(f"differential cases passed: {checked}")
