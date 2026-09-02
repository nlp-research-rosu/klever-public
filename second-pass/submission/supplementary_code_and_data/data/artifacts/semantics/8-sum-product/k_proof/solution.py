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
