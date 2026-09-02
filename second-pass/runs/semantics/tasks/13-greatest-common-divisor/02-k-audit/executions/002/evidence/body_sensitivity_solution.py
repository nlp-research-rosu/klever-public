def greatest_common_divisor(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)
    while b != 0:
        b = 0
    return a


# The altered body returns 6 for (6, 4), whereas gcdSpec(6, 4) reduces to 2.
assert greatest_common_divisor(6, 4) == 6
assert greatest_common_divisor(6, 4) != 2
