from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    result = []
    number = 0
    for number in numbers:
        if numbers.count(number) == 1:
            result.append(number)
    return result
