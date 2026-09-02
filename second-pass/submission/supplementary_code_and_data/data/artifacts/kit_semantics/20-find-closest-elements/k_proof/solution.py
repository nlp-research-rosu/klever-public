from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    if numbers[0] < numbers[1]:
        closest = (numbers[0], numbers[1])
    else:
        closest = (numbers[1], numbers[0])
    items = list(enumerate(numbers))
    item1 = items[0]
    item2 = items[0]
    for item1 in items:
        for item2 in items:
            if item1[0] < item2[0]:
                if abs(item2[1] - item1[1]) < abs(closest[1] - closest[0]):
                    if item1[1] < item2[1]:
                        closest = (item1[1], item2[1])
                    else:
                        closest = (item2[1], item1[1])
    return closest
