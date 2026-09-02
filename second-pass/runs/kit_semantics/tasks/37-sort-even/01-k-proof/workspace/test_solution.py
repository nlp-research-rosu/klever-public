from itertools import product

from solution import sort_even


def contract_oracle(values):
    expected = values[:]
    expected[::2] = sorted(expected[::2])
    return expected


def main():
    examples = [
        [],
        [7],
        [1, 2, 3],
        [5, 6, 3, 4],
        [9, -1, 4, -2, 4],
    ]
    tested = 0
    for values in examples:
        assert sort_even(values) == contract_oracle(values)
        tested += 1

    for length in range(7):
        for values in product(range(-2, 3), repeat=length):
            sample = list(values)
            assert sort_even(sample) == contract_oracle(sample)
            tested += 1

    print(f"Python differential tests: {tested} cases, 0 mismatches")


if __name__ == "__main__":
    main()
