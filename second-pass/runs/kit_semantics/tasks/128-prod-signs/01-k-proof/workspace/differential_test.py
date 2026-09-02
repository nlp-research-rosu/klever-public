from itertools import product

from solution import prod_signs


def independent_oracle(arr):
    if not arr:
        return None

    magnitude_sum = sum(abs(value) for value in arr)
    negative_count = sum(1 for value in arr if value < 0)
    has_zero = any(value == 0 for value in arr)

    if has_zero:
        product_of_signs = 0
    elif negative_count % 2 == 0:
        product_of_signs = 1
    else:
        product_of_signs = -1

    return magnitude_sum * product_of_signs


def main():
    values = range(-3, 4)
    case_count = 0
    mismatch_count = 0

    special_cases = [
        [1, 2, 2, -4],
        [0, 1],
        [],
        [10**100],
        [-(10**100)],
        [10**100, -(10**100)],
        [-(10**100), 0, 10**100],
        [-1, -2, -3],
    ]

    for arr in special_cases:
        case_count += 1
        if prod_signs(arr) != independent_oracle(arr):
            mismatch_count += 1

    for length in range(6):
        for values_tuple in product(values, repeat=length):
            arr = list(values_tuple)
            case_count += 1
            if prod_signs(arr) != independent_oracle(arr):
                mismatch_count += 1

    print(
        f"DIFFERENTIAL_CASES={case_count} "
        f"MISMATCHES={mismatch_count}"
    )
    if mismatch_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
