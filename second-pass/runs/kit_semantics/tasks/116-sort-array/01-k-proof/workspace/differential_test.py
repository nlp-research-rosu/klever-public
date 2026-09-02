import itertools
import random

from solution import sort_array


def arithmetic_popcount(value):
    value = abs(value)
    count = 0
    while value:
        value, bit = divmod(value, 2)
        count += bit
    return count


def independent_oracle(values):
    result = []
    for value in values:
        position = 0
        value_key = (arithmetic_popcount(value), value)
        while position < len(result):
            other = result[position]
            if value_key < (arithmetic_popcount(other), other):
                break
            position += 1
        result.insert(position, value)
    return result


def main():
    cases = [
        [],
        [0],
        [1, 5, 2, 3, 4],
        [-2, -3, -4, -5, -6],
        [1, 0, 2, 3, 4],
        [2, 5, 77, 4, 5, 3, 5, 7, 2, 3, 4],
        [3, 6, 44, 12, 32, 5],
        [2, 4, 8, 16, 32],
    ]

    alphabet = (-4, -3, -2, -1, 0, 1, 2, 3, 4)
    for length in range(5):
        cases.extend(list(values) for values in itertools.product(alphabet, repeat=length))

    rng = random.Random(116)
    for _ in range(2000):
        length = rng.randrange(0, 21)
        cases.append([rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)])

    mismatches = 0
    for values in cases:
        expected = independent_oracle(values)
        actual = sort_array(values)
        if actual != expected:
            mismatches += 1
            print("MISMATCH", values, expected, actual)
            break

    print(f"DIFFERENTIAL_CASES={len(cases)}")
    print(f"MISMATCHES={mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
