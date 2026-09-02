from typing import List


def mean_absolute_deviation(numbers: List[float]) -> float:
    """Return the mean absolute deviation of a non-empty list of numbers."""
    mean = sum(numbers) / len(numbers)
    total_deviation = 0.0
    for number in numbers:
        total_deviation += abs(number - mean)
    return total_deviation / len(numbers)
