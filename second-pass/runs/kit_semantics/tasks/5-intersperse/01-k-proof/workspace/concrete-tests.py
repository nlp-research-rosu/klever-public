from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    result = []
    for number in numbers:
        if result:
            result.append(delimeter)
        result.append(number)
    return result


empty_result = intersperse([], 4)
singleton_result = intersperse([1], 4)
example_result = intersperse([1, 2, 3], 4)
