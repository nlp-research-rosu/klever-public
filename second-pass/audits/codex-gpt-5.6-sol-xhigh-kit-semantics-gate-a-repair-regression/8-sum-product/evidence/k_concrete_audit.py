"""Reviewer-authored concrete checks for the supplied MPY semantics."""

from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    total = 0
    product = 1
    number = 0
    for number in numbers:
        total += number
        product *= number
    return (total, product)


# Empty-loop boundary, documented nonempty example, and negative/zero behavior.
assert sum_product([]) == (0, 1)
assert sum_product([1, 2, 3, 4]) == (10, 24)
assert sum_product([-2, 3, 0, 5]) == (6, 0)
