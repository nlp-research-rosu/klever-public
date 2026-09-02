def triangle_area(a, b, c):
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    s = (a + b + c) / 2
    return round((s * (s - a) * (s - b) * (s - c)) ** 0.5, 2)

assert triangle_area(2, 3, 3) == 2.83
