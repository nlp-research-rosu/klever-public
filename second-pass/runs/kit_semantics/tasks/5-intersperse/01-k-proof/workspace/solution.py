from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    result = []
    for number in numbers:
        if result:
            result.append(delimeter)
        result.append(number)
    return result
