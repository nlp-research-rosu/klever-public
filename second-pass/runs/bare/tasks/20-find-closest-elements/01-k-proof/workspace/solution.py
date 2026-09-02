from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    closest_a = numbers[0]
    closest_b = numbers[1]
    if closest_b < closest_a:
        temporary = closest_a
        closest_a = closest_b
        closest_b = temporary
    best_gap = closest_b - closest_a
    i = 0
    while i < len(numbers):
        j = i + 1
        while j < len(numbers):
            a = numbers[i]
            b = numbers[j]
            if b < a:
                temporary = a
                a = b
                b = temporary
            gap = b - a
            if gap < best_gap:
                best_gap = gap
                closest_a = a
                closest_b = b
            j = j + 1
        i = i + 1
    return (closest_a, closest_b)
