def triangle_area(a, b, c):
    if a + b <= c:
        return -1
    if a + c <= b:
        return -1
    if b + c <= a:
        return -1

    semiperimeter = (a + b + c) / 2
    area = (
        semiperimeter
        * (semiperimeter - a)
        * (semiperimeter - b)
        * (semiperimeter - c)
    ) ** 0.5
    return round(area, 2)
