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


assert rolling_max([]) == []
assert rolling_max([5]) == [5]
assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]
assert rolling_max([4, 3, 2, 1]) == [4, 4, 4, 4]
assert rolling_max([-3, -5, -2, -2]) == [-3, -3, -2, -2]
