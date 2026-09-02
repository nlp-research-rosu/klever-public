from itertools import product
from random import Random

from solution import by_length


NAMES = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
}


def oracle(arr):
    return [NAMES[value] for value in sorted(arr, reverse=True) if value in NAMES]


def cases():
    boundary_values = (-2, 0, 1, 2, 8, 9, 10)
    for length in range(5):
        yield from (list(items) for items in product(boundary_values, repeat=length))

    random = Random(20260725)
    for _ in range(2000):
        yield [random.randint(-100, 100) for _ in range(random.randint(0, 30))]


checked = 0
mismatches = 0
for case in cases():
    checked += 1
    if by_length(case) != oracle(case):
        mismatches += 1
        print("MISMATCH", case, by_length(case), oracle(case))

print(f"checked={checked} mismatches={mismatches}")
assert mismatches == 0
