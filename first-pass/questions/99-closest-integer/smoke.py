def closest_integer(value):
    from math import floor, ceil

    if value.count('.') == 1:
        # remove trailing zeros
        while (value[-1] == '0'):
            value = value[:-1]

    num = float(value)
    if value[-2:] == '.5':
        if num > 0:
            res = ceil(num)
        else:
            res = floor(num)
    elif len(value) > 0:
        res = int(round(num))
    else:
        res = 0

    return res


# Smoke checks — the HumanEval/99 dataset `check` cases (bare-value asserts).
assert closest_integer("10") == 10
assert closest_integer("15.3") == 15
assert closest_integer("14.5") == 15
assert closest_integer("-14.5") == -15
assert closest_integer("0.5") == 1
assert closest_integer("-0.4") == 0
assert closest_integer("2.50") == 3
assert closest_integer("-2.50") == -3
assert closest_integer("7.00") == 7
assert closest_integer("0") == 0
assert closest_integer("-100") == -100
assert closest_integer("3.7") == 4
assert closest_integer("5.") == 5
