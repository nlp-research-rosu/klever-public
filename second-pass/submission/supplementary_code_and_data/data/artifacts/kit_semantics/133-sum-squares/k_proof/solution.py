import math


def sum_squares(lst):
    total = 0
    number = 0
    rounded = 0
    for number in lst:
        rounded = math.ceil(number)
        total += rounded * rounded
    return total
