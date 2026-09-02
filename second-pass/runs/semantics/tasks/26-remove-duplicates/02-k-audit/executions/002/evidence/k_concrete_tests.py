from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    result = []
    for number in numbers:
        if numbers.count(number) == 1:
            result.append(number)
    return result


assert remove_duplicates([]) == []
assert remove_duplicates([1]) == [1]
assert remove_duplicates([1, 1]) == []
assert remove_duplicates([1, 1, 1]) == []
assert remove_duplicates([1, 2]) == [1, 2]
assert remove_duplicates([1, 2, 3, 2, 4]) == [1, 3, 4]
assert remove_duplicates([2, 1, 2]) == [1]
assert remove_duplicates([2, 1, 1]) == [2]
assert remove_duplicates([0, -1, 0, 2, -1, 3]) == [2, 3]
assert remove_duplicates([-999999999999999999999, 0, -999999999999999999999]) == [0]
