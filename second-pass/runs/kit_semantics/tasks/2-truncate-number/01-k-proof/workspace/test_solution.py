import math

from solution import truncate_number


def main() -> None:
    examples = [0.125, 0.5, 1.0, 3.5, 10.25, 123.875]
    grid = [
        whole + fraction / 16.0
        for whole in range(0, 101)
        for fraction in range(1, 16)
    ]
    inputs = examples + grid
    mismatches = []

    for number in inputs:
        expected = math.modf(number)[0]
        actual = truncate_number(number)
        if actual != expected:
            mismatches.append((number, actual, expected))

    print(f"inputs={len(inputs)} mismatches={len(mismatches)}")
    if mismatches:
        raise AssertionError(mismatches[:10])


if __name__ == "__main__":
    main()
