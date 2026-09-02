from typing import List


def mean_absolute_deviation(numbers: List[float]) -> float:
    count = len(numbers)
    if count == 0:
        return 0.0

    total = 0.0
    number = 0.0
    for number in numbers:
        total = total + number

    mean = total / count
    deviation = 0.0
    for number in numbers:
        deviation = deviation + abs(number - mean)

    return deviation / count


assert mean_absolute_deviation([]) == 0.0
assert mean_absolute_deviation([1.0]) == 0.0
assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0
