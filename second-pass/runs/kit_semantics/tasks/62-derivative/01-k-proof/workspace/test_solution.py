from itertools import product
from random import Random

from solution import derivative


def oracle(xs):
    return [index * value for index, value in enumerate(xs)][1:]


def main():
    cases = []
    alphabet = range(-2, 3)
    for length in range(6):
        cases.extend(list(values) for values in product(alphabet, repeat=length))

    random = Random(2807)
    for _ in range(1000):
        length = random.randrange(26)
        cases.append([random.randrange(-1000, 1001) for _ in range(length)])

    cases.extend(
        [
            [],
            [7],
            [1, 2, 3],
            [3, 1, 2, 4, 5],
            [0, -2, 4, -3],
            [1.0, 2.5, -3.0],
        ]
    )

    mismatches = 0
    for xs in cases:
        actual = derivative(xs)
        expected = oracle(xs)
        if actual != expected:
            mismatches += 1
            print("mismatch", xs, actual, expected)

    print(f"differential cases: {len(cases)}; mismatches: {mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
