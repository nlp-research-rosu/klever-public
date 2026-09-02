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


assert closest_integer("10") == 10
assert closest_integer("15.3") == 15
assert closest_integer("14.5") == 15
assert closest_integer("-14.5") == -15
assert closest_integer("0") == 0
assert closest_integer("0.49") == 0
assert closest_integer("-0.49") == 0
assert closest_integer("0.5") == 1
assert closest_integer("-0.5") == -1
assert closest_integer("2.499") == 2
assert closest_integer("-2.499") == -2
assert closest_integer("2.501") == 3
assert closest_integer("-2.501") == -3
assert closest_integer("999.499999") == 999
assert closest_integer("-999.499999") == -999
assert closest_integer("999.500001") == 1000
assert closest_integer("-999.500001") == -1000
assert closest_integer(".5") == 1
assert closest_integer("-.5") == -1
assert closest_integer("12.") == 12
assert closest_integer("-12.") == -12
assert closest_integer("0.49999999999999994") == 0
assert closest_integer("-0.49999999999999994") == 0
