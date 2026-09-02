def greatest_common_divisor(a: int, b: int) -> int:
    remainder = 0
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return abs(a)


result_3_5 = greatest_common_divisor(3, 5)
result_25_15 = greatest_common_divisor(25, 15)
result_zero_neg = greatest_common_divisor(0, -7)
result_both_zero = greatest_common_divisor(0, 0)

assert result_3_5 == 1
assert result_25_15 == 5
assert result_zero_neg == 7
assert result_both_zero == 0
