from typing import List


def mean_absolute_deviation(numbers: List[float]) -> float:
    """Return the mean absolute deviation of a non-empty list of numbers."""
    mean = sum(numbers) / len(numbers)
    total_deviation = 0.0
    for number in numbers:
        total_deviation += abs(number - mean)
    return total_deviation / len(numbers)


assert mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]) == 1.0
assert mean_absolute_deviation([7.25]) == 0.0
assert mean_absolute_deviation([-1.0, 1.0]) == 1.0
assert mean_absolute_deviation([-2.0, 0.0, 2.0]) == 1.3333333333333333
