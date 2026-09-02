from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    result = []
    for number in numbers:
        if result:
            result.append(delimeter)
        result.append(number)
    return result


assert intersperse([], 4) == []
assert intersperse([7], -2) == [7]
assert intersperse([1, 2], 9) == [1, 9, 2]
assert intersperse([1, 2, 3], 4) == [1, 4, 2, 4, 3]
assert intersperse([0, 0], 0) == [0, 0, 0]
assert intersperse([-1, 0, 1], -99) == [-1, -99, 0, -99, 1]
