def derivative(xs: list):
    """Return the coefficients of the derivative of a polynomial."""
    result = []
    for i, x in enumerate(xs):
        if i > 0:
            result.append(i * x)
    return result
