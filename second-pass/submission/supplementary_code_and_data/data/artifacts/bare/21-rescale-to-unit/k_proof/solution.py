from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:
    minimum = min(numbers)
    maximum = max(numbers)
    return [
        (number - minimum) / (maximum - minimum)
        for number in numbers
    ]
