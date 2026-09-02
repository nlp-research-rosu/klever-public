def add(lst):
    """Add the even elements that occur at odd zero-based indices."""
    total = 0
    odd_index = False
    value = 0
    for value in lst:
        if odd_index:
            if value % 2 == 0:
                total += value
        odd_index = not odd_index
    return total


assert add([4, 2, 6, 7]) == 2
assert add([2]) == 0
assert add([1, 2]) == 2
assert add([1, 3, 4, -6, 8, 10]) == 4
assert add([-2, -4, -6, -8]) == -12
assert add([0, 0, 0, 0]) == 0
