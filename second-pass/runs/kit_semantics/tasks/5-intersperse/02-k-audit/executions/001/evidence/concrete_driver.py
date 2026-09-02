from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    result = []
    for number in numbers:
        if result:
            result.append(delimeter)
        result.append(number)
    return result


empty_result = intersperse([], 4)
singleton_result = intersperse([7], -2)
two_result = intersperse([7, 8], -2)
documented_result = intersperse([1, 2, 3], 4)
zeros_result = intersperse([0, 0, 0], 0)
negative_result = intersperse([-3, -1, 2], -3)
