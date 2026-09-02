import math


def sum_squares(lst):
    result = 0
    for number in lst:
        result += math.ceil(number) ** 2
    return result


# Satisfying ground instances used for the function claim and loop invariant.
assert sum_squares([]) == 0
assert sum_squares([1, 2, 3]) == 14
assert sum_squares([1.4, 4.2, 0]) == 29
assert sum_squares([-2.4, 1, 1]) == 6
assert sum_squares([-1.000000001, -0.999999999, 1.000000001]) == 5
