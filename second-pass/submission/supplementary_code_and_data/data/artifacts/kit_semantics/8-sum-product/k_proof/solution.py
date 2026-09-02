from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    total = 0
    product = 1
    for number in numbers:
        total += number
        product *= number
    return (total, product)
