from typing import List, Tuple
from math import prod


def sum_product(numbers: List[int]) -> Tuple[int, int]:
    return (sum(numbers), prod(numbers))
