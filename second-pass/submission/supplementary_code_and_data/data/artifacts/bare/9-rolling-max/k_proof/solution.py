from typing import List, Tuple


def rolling_max(numbers: List[int]) -> List[int]:
    result = []
    first = True
    maximum = 0
    for number in numbers:
        if first:
            maximum = number
            first = False
        else:
            if number > maximum:
                maximum = number
        result.append(maximum)
    return result
