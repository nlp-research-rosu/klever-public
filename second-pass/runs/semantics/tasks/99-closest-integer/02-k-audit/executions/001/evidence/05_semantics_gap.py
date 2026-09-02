def closest_integer(value):
    number = float(value)
    if number > 0.0:
        return int(number + 0.5)
    return int(number - 0.5)


# CPython accepts this numeric string and returns 1. The supplied K decimal
# parser documents only digits/dot with optional leading minus.
assert closest_integer("5e-1") == 1
