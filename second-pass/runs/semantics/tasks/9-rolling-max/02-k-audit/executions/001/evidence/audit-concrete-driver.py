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


assert rolling_max([]) == []
assert rolling_max([7]) == [7]
assert rolling_max([4, 3]) == [4, 4]
assert rolling_max([4, 4]) == [4, 4]
assert rolling_max([3, 4]) == [3, 4]
assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]
assert rolling_max([-8, -9, -3, -3, -10]) == [-8, -8, -3, -3, -3]
assert rolling_max([100000000000000000000, -100000000000000000000, 1000000000000000000000]) == [100000000000000000000, 100000000000000000000, 1000000000000000000000]
