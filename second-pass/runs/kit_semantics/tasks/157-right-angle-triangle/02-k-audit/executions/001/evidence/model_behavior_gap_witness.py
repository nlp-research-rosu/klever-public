def right_angle_triangle(a, b, c):
    return (
        a * a == b * b + c * c
        or b * b == a * a + c * c
        or c * c == a * a + b * b
    )


# These are three positive, equal side lengths (an equilateral, non-right
# triangle). CPython raises OverflowError when a later mixed addition attempts
# to coerce the already-squared unbounded integer (10**616) to binary64. The
# supplied MPY model declares intToF total and has no exception transition.
result = right_angle_triangle(10 ** 308, 1.0e308, 1.0e308)
