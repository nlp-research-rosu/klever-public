from math import ceil


def sum_squares(lst):
    total = 0
    for number in lst:
        rounded = ceil(number)
        total += rounded * rounded
    return total
