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
