from itertools import product

from solution import solution


def oracle(values):
    return sum(
        value
        for position, value in enumerate(values)
        if position % 2 == 0 and value % 2 != 0
    )


checked = 0
for length in range(1, 6):
    for values in product(range(-3, 4), repeat=length):
        candidate = solution(list(values))
        expected = oracle(values)
        assert candidate == expected, (values, candidate, expected)
        checked += 1

print(f"Differential cases: {checked}; mismatches: 0")
