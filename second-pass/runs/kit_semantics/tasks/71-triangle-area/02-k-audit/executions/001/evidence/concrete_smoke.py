import math


def triangle_area(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return -1

    semi_perimeter = (a + b + c) / 2
    area = math.sqrt(
        semi_perimeter
        * (semi_perimeter - a)
        * (semi_perimeter - b)
        * (semi_perimeter - c)
    )
    return round(area, 2)


assert triangle_area(3, 4, 5) == 6.0
assert triangle_area(1, 2, 10) == -1
assert triangle_area(1, 2, 3) == -1
assert triangle_area(1, 3, 2) == -1
assert triangle_area(3, 1, 2) == -1
assert triangle_area(2, 2, 3) == 1.98
assert triangle_area(2.5, 3.0, 4.0) == 3.75
assert triangle_area(True, True, True) == 0.43
