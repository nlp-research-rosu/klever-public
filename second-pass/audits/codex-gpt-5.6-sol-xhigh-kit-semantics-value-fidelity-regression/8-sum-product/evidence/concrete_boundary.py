from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    sum_value = 0
    product_value = 1
    number = 0
    for number in numbers:
        sum_value += number
        product_value *= number
    return (sum_value, product_value)


assert sum_product([]) == (0, 1)
assert sum_product([7]) == (7, 7)
assert sum_product([0]) == (0, 0)
assert sum_product([-1]) == (-1, -1)
assert sum_product([1, 2, 3, 4]) == (10, 24)
assert sum_product([-2, 3, 0, 5]) == (6, 0)
assert sum_product([-2, -3]) == (-5, 6)
