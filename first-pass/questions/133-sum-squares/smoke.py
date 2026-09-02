def sum_squares(lst):
    import math
    squared = 0
    i = 0
    for i in lst:
        squared += math.ceil(i) ** 2
    return squared


assert sum_squares([1, 2, 3]) == 14
assert sum_squares([1.0, 2, 3]) == 14
assert sum_squares([1.4, 4.2, 0]) == 29
assert sum_squares([-2.4, 1, 1]) == 6
assert sum_squares([-1.4, 4.6, 6.3]) == 75
