from typing import List


def is_close_to_any(number: float, numbers: List[float], threshold: float, start: int) -> bool:
    found = False
    index = 0
    other = number
    for other in numbers:
        if index >= start:
            if abs(number - other) < threshold:
                found = True
                break
        index += 1
    index = 0
    other = number
    return found


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    found = False
    start = 1
    number = threshold
    for number in numbers:
        if is_close_to_any(number, numbers, threshold, start):
            found = True
            break
        start += 1
    start = 1
    number = threshold
    return found
