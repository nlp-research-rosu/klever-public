from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    result = False
    i = 0
    j = 0
    elem = 0.0
    elem2 = 0.0

    for elem in numbers:
        j = 0
        for elem2 in numbers:
            if i != j:
                if abs(elem - elem2) < threshold:
                    result = True
            j = j + 1
            elem2 = 0.0
        i = i + 1
        j = 0
        elem = 0.0

    return result


assert has_close_elements([1.0, 2.0, 3.0], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
assert has_close_elements([], 0.5) == False
assert has_close_elements([4.0], 1.0) == False
assert has_close_elements([0.0, 1.0], 1.0) == False
assert has_close_elements([0.0, 1.0], 1.1) == True
assert has_close_elements([2.0, 2.0], 0.0) == False
assert has_close_elements([2.0, 2.0], 0.0001) == True
assert has_close_elements([0.0, 0.1, 100.0, 200.0], 0.2) == True
assert has_close_elements([0.0, 0.0], -1.0) == False
