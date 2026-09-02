def triangle_area(a, h):
    return a * h / 2.0


assert triangle_area(5, 3) == 7.5
assert triangle_area(0, 9) == 0.0
assert triangle_area(-4, 3) == -6.0
assert triangle_area(2.5, 4) == 5.0
assert triangle_area(3, 2.5) == 3.75
assert triangle_area(2.5, 1.5) == 1.875
