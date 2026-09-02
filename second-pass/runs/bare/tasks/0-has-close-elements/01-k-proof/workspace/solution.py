from typing import List


def close_to_first(first, rest, threshold):
    if len(rest) == 0:
        return False
    if abs(first - rest[0]) < threshold:
        return True
    return close_to_first(first, rest[1:], threshold)


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    if len(numbers) < 2:
        return False
    if close_to_first(numbers[0], numbers[1:], threshold):
        return True
    return has_close_elements(numbers[1:], threshold)
