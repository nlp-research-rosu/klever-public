def right_angle_triangle(a, b, c):
    return (
        a * a == b * b + c * c
        or b * b == a * a + c * c
        or c * c == a * a + b * b
    )


assert right_angle_triangle(3, 4, 5) == True
assert right_angle_triangle(1, 2, 3) == False
assert right_angle_triangle(5, 12, 13) == True
assert right_angle_triangle(6, 8, 10) == True
assert right_angle_triangle(2, 2, 3) == False
assert right_angle_triangle(3.0, 4.0, 5.0) == True
assert right_angle_triangle(1.5, 2.0, 2.5) == True
assert right_angle_triangle(3, 4.0, 5) == True
assert right_angle_triangle(1.0, 2, 3.0) == False
assert right_angle_triangle(0.3, 0.4, 0.5) == True
