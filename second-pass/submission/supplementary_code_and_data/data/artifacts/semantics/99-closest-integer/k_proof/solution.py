def closest_integer(value):
    number = float(value)
    if number > 0.0:
        return int(number + 0.5)
    return int(number - 0.5)
