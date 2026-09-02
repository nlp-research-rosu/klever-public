def triangle_area(a, h):
    return a * h / 2


# CPython raises OverflowError while converting this unbounded integer result
# to binary64 for true division. The supplied semantics has no OverflowError.
triangle_area(10**400, 1)
