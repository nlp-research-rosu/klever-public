from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """Return the sum and product of all integers in numbers."""
    total = 0
    product = 1
    number = 0
    for number in numbers:
        total += number
        product *= number
    return (total, product)


assert sum_product([]) == (0, 1)
assert sum_product([1, 2, 3, 4]) == (10, 24)
assert sum_product([-2, 3, 0]) == (1, 0)
assert sum_product([-2, -3, 4]) == (-1, 24)
assert sum_product([10**20, -3, 2]) == (99999999999999999999, -600000000000000000000)
