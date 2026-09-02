import math


def closest_integer(value):
    number = float(value)
    lower = math.floor(number)
    upper = math.ceil(number)
    if number > 0:
        if number - lower < 0.5:
            return lower
        return upper
    if upper - number < 0.5:
        return upper
    return lower
