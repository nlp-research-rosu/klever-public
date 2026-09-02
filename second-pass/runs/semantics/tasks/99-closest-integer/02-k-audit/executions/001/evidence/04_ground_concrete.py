def closest_integer(value):
    number = float(value)
    if number > 0.0:
        return int(number + 0.5)
    return int(number - 0.5)


assert closest_integer("10") == 10
assert closest_integer("0.49999999999999994") == 1
