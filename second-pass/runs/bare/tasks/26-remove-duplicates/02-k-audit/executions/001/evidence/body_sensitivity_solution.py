from typing import List


def remove_duplicates(numbers: List[int]) -> List[int]:
    # Deliberate body mutation: keep values occurring exactly twice.
    return [number for number in numbers if numbers.count(number) == 2]
