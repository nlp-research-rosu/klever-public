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
