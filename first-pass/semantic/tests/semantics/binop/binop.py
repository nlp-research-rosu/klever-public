# BinOp: + - * % // on Int. % and // are Python-FLOORED (result takes the sign of
# the DIVISOR); all four sign combinations are checked — the negative-divisor cases
# (7 % -3, 7 // -3) are what K's modInt (Euclidean) gets wrong.
assert 2 + 3 == 5
assert 5 - 8 == -3
assert 6 * 7 == 42
assert -7 % 3 == 2
assert 7 % -3 == -2
assert -7 % -3 == -1
assert 7 % 3 == 1
assert -7 // 3 == -3
assert 7 // -3 == -3
assert -7 // -3 == 2
assert 7 // 3 == 2

# ** integer power (non-negative exponent; negative exponent is a float -> unsupported)
assert 2 ** 5 == 32
assert 3 ** 3 == 27
assert 2 ** 0 == 1
assert 0 ** 0 == 1
assert 0 ** 5 == 0
assert 10 ** 3 == 1000
assert (-2) ** 2 == 4
assert (-2) ** 3 == -8
