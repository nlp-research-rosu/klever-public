def evaluate_polynomial(xs: list, x):
    value = 0
    power = 1
    for coefficient in xs:
        value = value + coefficient * power
        power = power * x
    return value


def find_zero(xs: list):
    left = -1
    right = 1

    while evaluate_polynomial(xs, left) * evaluate_polynomial(xs, right) > 0:
        left = left * 2
        right = right * 2

    while right - left > 1 / 10000000000:
        middle = (left + right) / 2
        if evaluate_polynomial(xs, middle) * evaluate_polynomial(xs, left) > 0:
            left = middle
        else:
            right = middle

    return (left + right) / 2
