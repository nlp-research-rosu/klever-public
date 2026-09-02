from typing import List


def rolling_max(numbers: List[int]) -> List[int]:
    """Return the maximum seen at each position in numbers."""
    result = []
    if numbers:
        current = numbers[0]
        number = current
        for number in numbers:
            if number > current:
                current = number
            result.append(current)
    return result
