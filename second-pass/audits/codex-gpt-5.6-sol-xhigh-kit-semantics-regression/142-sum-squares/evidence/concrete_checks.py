def sum_squares(lst):
    total = 0
    index = 0
    value = 0
    for value in lst:
        if index % 3 == 0:
            total = total + value * value
        elif index % 4 == 0:
            total = total + value * value * value
        else:
            total = total + value
        index = index + 1
    return total


assert sum_squares([]) == 0
assert sum_squares([1, 2, 3]) == 6
assert sum_squares([-1, -5, 2, -1, -5]) == -126
assert sum_squares([2, -3, 5, -7, 11]) == 1386
assert sum_squares([2, -3, 5, -7, 11, -13, 17, -19, 23, -29, 31, -37, 41]) == 16326
