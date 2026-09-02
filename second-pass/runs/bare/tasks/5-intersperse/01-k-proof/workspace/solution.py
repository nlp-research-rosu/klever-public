from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    if len(numbers) <= 1:
        return numbers
    return [numbers[0], delimeter] + intersperse(numbers[1:], delimeter)
