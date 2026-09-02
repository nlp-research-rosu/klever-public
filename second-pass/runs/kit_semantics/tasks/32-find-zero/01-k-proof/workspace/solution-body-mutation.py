def poly(xs: list, x: float):
    value = 0.0
    power = 1.0
    coeff = 0.0
    for coeff in xs:
        value = value + coeff * power
        power = power + x
    return value


def find_zero(xs: list):
    begin = len(xs) / -len(xs)
    end = len(xs) / len(xs)
    center = 0.0
    while poly(xs, begin) * poly(xs, end) > 0.0:
        begin = begin * 2.0
        end = end * 2.0
    while end - begin > 0.0000000001:
        center = (begin + end) / 2.0
        if poly(xs, center) * poly(xs, begin) > 0.0:
            begin = center
        else:
            end = center
    return begin
