def closest_integer(value):
    number = float(value)
    if number > 0.0:
        return int(number + 0.5)
    return int(number - 0.5)


assert closest_integer("9007199254740991") == 9007199254740992
assert closest_integer("-9007199254740991") == -9007199254740992
assert closest_integer("2.499999999999999999") == 3
assert closest_integer("-2.499999999999999999") == -3
assert closest_integer("1e1") == 631
