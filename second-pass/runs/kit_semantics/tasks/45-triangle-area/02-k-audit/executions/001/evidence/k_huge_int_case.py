def triangle_area(a, h):
    return a * h / 2.0


# CPython raises OverflowError when true division converts this integer to float.
triangle_area(2**1024, 1)
