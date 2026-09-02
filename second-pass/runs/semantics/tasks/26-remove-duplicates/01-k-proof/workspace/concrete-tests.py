from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    result = []
    for number in numbers:
        if numbers.count(number) == 1:
            result.append(number)
    return result


assert remove_duplicates([]) == []
assert remove_duplicates([1]) == [1]
assert remove_duplicates([1, 2, 3, 2, 4]) == [1, 3, 4]
assert remove_duplicates([1, 1]) == []
assert remove_duplicates([3, 1, 3, 2, 2, 4]) == [1, 4]
assert remove_duplicates([-1, 0, -1, 2]) == [0, 2]
