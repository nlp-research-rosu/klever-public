def right_angle_triangle(a, b, c):
    return a*a == b*b + c*c or b*b == a*a + c*c or c*c == a*a + b*b


# HumanEval/157 test cases (the dataset `check`); returns a bool.
assert right_angle_triangle(3, 4, 5)
assert not right_angle_triangle(1, 2, 3)
assert right_angle_triangle(10, 6, 8)
assert not right_angle_triangle(2, 2, 2)
assert right_angle_triangle(7, 24, 25)
assert not right_angle_triangle(10, 5, 7)
assert right_angle_triangle(5, 12, 13)
assert right_angle_triangle(15, 8, 17)
assert right_angle_triangle(48, 55, 73)
assert not right_angle_triangle(1, 1, 1)
assert not right_angle_triangle(2, 2, 10)
