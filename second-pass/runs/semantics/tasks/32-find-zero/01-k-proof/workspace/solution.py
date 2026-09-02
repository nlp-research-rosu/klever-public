import math


def poly(xs: list, x: float):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs: list):
    begin = -1
    end = 1

    while poly(xs, begin) * poly(xs, end) > 0:
        begin *= 2
        end *= 2

    while end - begin > 1e-10:
        center = (begin + end) / 2
        if poly(xs, center) * poly(xs, begin) > 0:
            begin = center
        else:
            end = center

    return begin
