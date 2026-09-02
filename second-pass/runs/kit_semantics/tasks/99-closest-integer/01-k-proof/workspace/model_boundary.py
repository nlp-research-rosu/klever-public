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


# The reference semantics' decimal parser intentionally does not model
# exponent notation: it interprets the character codes in "1e2" as 632.
assert closest_integer("1e2") == 632
