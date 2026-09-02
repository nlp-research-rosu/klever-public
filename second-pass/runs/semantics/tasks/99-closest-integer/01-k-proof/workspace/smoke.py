def closest_integer(value):
    number = float(value)
    if number > 0.0:
        return int(number + 0.5)
    return int(number - 0.5)


assert closest_integer("10") == 10
assert closest_integer("15.3") == 15
assert closest_integer("14.5") == 15
assert closest_integer("-14.5") == -15
assert closest_integer("-14.4") == -14
assert closest_integer("0.5") == 1
assert closest_integer("-0.5") == -1
assert closest_integer("0") == 0
