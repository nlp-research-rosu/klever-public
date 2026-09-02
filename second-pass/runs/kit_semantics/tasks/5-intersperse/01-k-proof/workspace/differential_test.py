from itertools import product

from solution import intersperse


def oracle(numbers, delimeter):
    expected = []
    for index, number in enumerate(numbers):
        if index > 0:
            expected += [delimeter]
        expected += [number]
    return expected


def main():
    values = (-2, -1, 0, 1, 2)
    delimiters = (-2, -1, 0, 1, 2)
    cases = 0
    mismatches = 0

    for length in range(6):
        for numbers in product(values, repeat=length):
            for delimeter in delimiters:
                cases += 1
                actual = intersperse(list(numbers), delimeter)
                expected = oracle(numbers, delimeter)
                if actual != expected:
                    mismatches += 1

    print(f"cases={cases} mismatches={mismatches}")
    if mismatches != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
