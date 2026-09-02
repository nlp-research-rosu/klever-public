def multiply(a, b):
    return (a % 10) * (b % 10)


assert multiply(148, 412) == 16
assert multiply(19, 28) == 72
assert multiply(2020, 1851) == 0
assert multiply(14, -15) == 20
assert multiply(-14, 15) == 30
assert multiply(-14, -15) == 30
