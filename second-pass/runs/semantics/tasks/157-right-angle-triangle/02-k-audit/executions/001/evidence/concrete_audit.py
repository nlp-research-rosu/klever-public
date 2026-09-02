def right_angle_triangle(a, b, c):
    if a <= 0:
        return False
    if b <= 0:
        return False
    if c <= 0:
        return False
    if a * a + b * b == c * c:
        return True
    if a * a + c * c == b * b:
        return True
    if b * b + c * c == a * a:
        return True
    return False


assert right_angle_triangle(3, 4, 5)
assert right_angle_triangle(3, 5, 4)
assert right_angle_triangle(5, 3, 4)
assert not right_angle_triangle(1, 2, 3)
assert not right_angle_triangle(0, 4, 4)
assert not right_angle_triangle(4, 0, 4)
assert not right_angle_triangle(4, 4, 0)
assert not right_angle_triangle(-3, 4, 5)
