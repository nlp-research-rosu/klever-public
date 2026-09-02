from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    total = 0
    product = 1
    for number in numbers:
        total += number
        product *= number
    return (total, product)


empty_result = sum_product([])
example_result = sum_product([1, 2, 3, 4])
signed_result = sum_product([-2, 3, -4])
zero_result = sum_product([0, 99])
