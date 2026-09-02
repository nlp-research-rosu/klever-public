def greatest_common_divisor(a: int, b: int) -> int:
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    r = 0
    while b != 0:
        r = a % b
        a = b
        b = r
    return a
