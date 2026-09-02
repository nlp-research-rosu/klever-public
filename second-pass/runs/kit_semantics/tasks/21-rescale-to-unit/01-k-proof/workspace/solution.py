from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:
    min_number = min(numbers)
    max_number = max(numbers)
    result = []
    number = numbers[0]
    for number in numbers:
        result.append(
            (number - min_number) / (max_number - min_number)
        )
    return result
