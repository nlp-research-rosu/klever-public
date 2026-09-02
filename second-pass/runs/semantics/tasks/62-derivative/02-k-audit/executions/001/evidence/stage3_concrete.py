def derivative(xs: list):
    """Return the coefficients of the derivative of a polynomial."""
    result = []
    for i, x in enumerate(xs):
        if i > 0:
            result.append(i * x)
    return result


# Expected values were computed independently from /reference/canonical.py.
assert derivative([3, 1, 2, 4, 5]) == [1, 4, 12, 20]
assert derivative([]) == []
assert derivative([7]) == []
assert derivative([0, 9]) == [9]
assert derivative([9, 0]) == [0]
assert derivative([0, -2, 5]) == [-2, 10]
assert derivative([-4, -3, -2, -1]) == [-3, -4, -3]
