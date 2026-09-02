from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    best_low = numbers[0]
    best_high = numbers[1]
    if best_low > best_high:
        best_low, best_high = best_high, best_low

    low = best_low
    high = best_high
    i = 0
    j = 1
    while i < len(numbers) - 1:
        low = numbers[i]
        high = numbers[j]
        if low > high:
            low, high = high, low
        if high - low < best_high - best_low:
            best_low = low
            best_high = high

        j += 1
        if j == len(numbers):
            i += 1
            j = i + 1
        low = best_low
        high = best_high

    return (best_low, best_high)


assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2]) == (2.0, 2.2)
assert find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0]) == (2.0, 2.0)
assert find_closest_elements([-4.5, -1.0]) == (-4.5, -1.0)
assert find_closest_elements([9.0, -2.0, 4.0]) == (4.0, 9.0)
