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


assert rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0]) == [
    0.0, 0.25, 0.5, 0.75, 1.0
]
assert rescale_to_unit([2.0, 1.0]) == [1.0, 0.0]
assert rescale_to_unit([-3.0, 7.0]) == [0.0, 1.0]
assert rescale_to_unit([3.0, 1.0, 3.0, 2.0]) == [
    1.0, 0.0, 1.0, 0.5
]
