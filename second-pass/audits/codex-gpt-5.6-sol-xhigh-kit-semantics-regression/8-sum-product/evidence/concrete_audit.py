from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    total = 0
    product = 1
    number = 0
    for number in numbers:
        total += number
        product *= number
    return total, product


assert sum_product([]) == (0, 1)
assert sum_product([1, 2, 3, 4]) == (10, 24)
assert sum_product([-7]) == (-7, -7)
assert sum_product([-2, 0, 5]) == (3, 0)
assert sum_product([-2, 3, -4]) == (-3, 24)
assert sum_product([9223372036854775807, -9223372036854775808, 1]) == (
    0,
    -85070591730234615856620279821087277056,
)
