from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    result = False
    i = 0
    number = 0.0
    j = 0
    other = 0.0
    for number in numbers:
        j = 0
        for other in numbers:
            if i < j:
                if abs(number - other) < threshold:
                    result = True
            j = j + 1
        i = i + 1
    return result


assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
assert has_close_elements([], 1.0) == False
assert has_close_elements([1.0], 1.0) == False
assert has_close_elements([0.0, 1.0], 1.0) == False
assert has_close_elements([0.0, 0.999], 1.0) == True
assert has_close_elements([1.0, 1.0], 0.0) == False
assert has_close_elements([1.0, 1.0], 0.01) == True
assert has_close_elements([-2.0, -1.9], -0.1) == False
