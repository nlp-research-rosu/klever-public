def derivative(xs: list):
    return derivative_helper(xs[1:], 1)


def derivative_helper(xs: list, degree: int):
    if xs == []:
        return []
    else:
        return [degree * xs[0]] + derivative_helper(xs[1:], degree + 1)
