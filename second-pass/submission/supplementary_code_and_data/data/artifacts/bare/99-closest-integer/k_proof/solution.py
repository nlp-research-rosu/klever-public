from decimal import Decimal


def closest_integer(value):
    number = Decimal(value)
    half = Decimal("0.5")
    if number >= 0:
        return int(number + half)
    return int(number - half)
