from itertools import product
from random import Random

from solution import get_row


def oracle(lst, x):
    result = []
    for row_index, row in enumerate(lst):
        for column_index in range(len(row) - 1, -1, -1):
            if row[column_index] == x:
                result.append((row_index, column_index))
    return result


def check_case(lst, x):
    actual = get_row(lst, x)
    expected = oracle(lst, x)
    if actual != expected:
        raise AssertionError(
            f"mismatch for lst={lst!r}, x={x!r}: "
            f"actual={actual!r}, expected={expected!r}"
        )


def main():
    values = (-1, 0, 1)
    rows = [[]]
    for length in range(1, 4):
        rows.extend([list(items) for items in product(values, repeat=length)])

    exhaustive = 0
    for row_count in range(4):
        for matrix_rows in product(rows, repeat=row_count):
            matrix = [row[:] for row in matrix_rows]
            for x in values:
                check_case(matrix, x)
                exhaustive += 1

    rng = Random(20260725)
    random_cases = 2000
    for _ in range(random_cases):
        matrix = [
            [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
            for _ in range(rng.randint(0, 10))
        ]
        check_case(matrix, rng.randint(-20, 20))

    print(
        f"differential: {exhaustive} exhaustive small cases + "
        f"{random_cases} seeded larger cases; mismatches=0"
    )


if __name__ == "__main__":
    main()
