from typing import List


def rolling_max(numbers: List[int]) -> List[int]:
    """Return the maximum seen so far at every position in numbers."""
    result = []
    first = True
    maximum = 0
    number = 0
    for number in numbers:
        if first:
            maximum = number
            first = False
        else:
            maximum = max(maximum, number)
        result.append(maximum)
    return result
