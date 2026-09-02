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
assert rolling_max([7]) == [7]
assert rolling_max([1, 1]) == [1, 1]
assert rolling_max([2, 1]) == [2, 2]
assert rolling_max([1, 2]) == [1, 2]
assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]
assert rolling_max([-9, -9, -3, -7, 0]) == [-9, -9, -3, -3, 0]
assert rolling_max([100000000000000000000, -1, 100000000000000000001]) == [
    100000000000000000000,
    100000000000000000000,
    100000000000000000001,
]
