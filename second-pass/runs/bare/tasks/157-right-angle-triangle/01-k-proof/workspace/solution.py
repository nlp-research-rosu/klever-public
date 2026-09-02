def right_angle_triangle(a, b, c):
    return a > 0 and b > 0 and c > 0 and (
        a * a + b * b == c * c
        or a * a + c * c == b * b
        or b * b + c * c == a * a
    )
