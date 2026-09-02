import math


def sum_squares(lst):
    result = 0
    for number in lst:
        result += math.ceil(number) ** 2
    return result


assert sum_squares([1, 2, 3]) == 14
assert sum_squares([1, 4, 9]) == 98
assert sum_squares([1, 3, 5, 7]) == 84
assert sum_squares([1.4, 4.2, 0]) == 29
assert sum_squares([-2.4, 1, 1]) == 6
assert sum_squares([]) == 0
