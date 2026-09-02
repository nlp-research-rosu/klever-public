from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    """Loop-body sensitivity witness: compare every gap with zero."""
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
        if high - low < best_high - best_high:
            best_low = low
            best_high = high

        j += 1
        if j == len(numbers):
            i += 1
            j = i + 1
        low = best_low
        high = best_high

    return (best_low, best_high)


# Under the fixed semantics the mutation preserves the initial pair.
assert find_closest_elements([1.0, 10.0, 2.0]) == (1.0, 10.0)
