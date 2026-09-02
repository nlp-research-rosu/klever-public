from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    found = False
    i = 0
    j = 0
    number1 = 0.0
    number2 = 0.0
    for number1 in numbers:
        j = 0
        for number2 in numbers:
            if i < j:
                if abs(number1 - number2) < threshold:
                    found = True
            j = j + 1
        i = i + 1
    return found


assert has_close_elements([], 0.5) == False
assert has_close_elements([1.0], 1.0) == False
assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
assert has_close_elements([1.0, 1.0], 0.0) == False
assert has_close_elements([1.0, 1.0], 0.1) == True
