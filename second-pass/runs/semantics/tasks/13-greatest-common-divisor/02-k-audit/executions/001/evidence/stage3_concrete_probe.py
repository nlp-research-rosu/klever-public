def greatest_common_divisor(a: int, b: int) -> int:
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a


assert greatest_common_divisor(3, 5) == 1
assert greatest_common_divisor(25, 15) == 5
assert greatest_common_divisor(0, 0) == 0
assert greatest_common_divisor(1, 0) == 1
assert greatest_common_divisor(0, -9) == 9
assert greatest_common_divisor(-54, 24) == 6
assert greatest_common_divisor(54, -24) == 6
assert greatest_common_divisor(-54, -24) == 6
assert greatest_common_divisor(35, 64) == 1
