from itertools import product
from random import Random

from solution import add


def oracle(values):
    total = 0
    for index, value in enumerate(values):
        if index % 2 == 1 and value % 2 == 0:
            total += value
    return total


def main():
    checked = 0
    mismatches = 0

    examples = [
        [4, 2, 6, 7],
        [10],
        [1, -2, 3, -4, 5, 8],
        [0, 0],
        [-8, -6, -4, -2],
    ]
    for values in examples:
        checked += 1
        mismatches += add(values) != oracle(values)

    alphabet = range(-3, 4)
    for length in range(1, 6):
        for values in product(alphabet, repeat=length):
            checked += 1
            mismatches += add(list(values)) != oracle(values)

    random = Random(20260729)
    for _ in range(1000):
        length = random.randint(1, 40)
        values = [random.randint(-1000, 1000) for _ in range(length)]
        checked += 1
        mismatches += add(values) != oracle(values)

    print(f"checked={checked} mismatches={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
