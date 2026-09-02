def triangle_area(a, h):
    return a * h / 2


assert triangle_area(5, 3) == 7.5
assert triangle_area(0, 0) == 0.0
assert triangle_area(-3, 6) == -9.0
assert triangle_area(3, 3) == 4.5
assert triangle_area(9007199254740991, 2) == 9007199254740991.0
