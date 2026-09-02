def multiply(a, b):
    return (a % 10) * (b % 10)


assert multiply(148, 412) == 16
assert multiply(19, 28) == 72
assert multiply(2020, 1851) == 0
assert multiply(14, -15) == 20
assert multiply(0, 0) == 0
assert multiply(9, 9) == 81
assert multiply(9, 10) == 0
assert multiply(10, 9) == 0
assert multiply(-9, 9) == 9
assert multiply(-10, 9) == 0
assert multiply(-11, 9) == 81
assert multiply(-9, -9) == 1
assert multiply(-10, -10) == 0
assert multiply(-11, -11) == 81
