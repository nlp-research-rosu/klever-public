from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    result = []
    number = 0
    for number in numbers:
        if numbers.count(number) == 1:
            result.append(number)
    return result


assert remove_duplicates([]) == []
assert remove_duplicates([0]) == [0]
assert remove_duplicates([7, 7]) == []
assert remove_duplicates([1, 2, 3, 2, 4]) == [1, 3, 4]
assert remove_duplicates([-2, 0, -2, 3, 0, 4]) == [3, 4]
assert remove_duplicates([100000000000000000000, -100000000000000000000, 5]) == [
    100000000000000000000,
    -100000000000000000000,
    5,
]
