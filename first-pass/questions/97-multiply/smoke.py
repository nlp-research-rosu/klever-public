def multiply(a, b):
    return abs(a % 10) * abs(b % 10)


# HumanEval/97 test cases (the dataset `check`); returns an int.
assert multiply(148, 412) == 16
assert multiply(19, 28) == 72
assert multiply(2020, 1851) == 0
assert multiply(14, -15) == 20
assert multiply(76, 67) == 42
assert multiply(17, 27) == 49
assert multiply(0, 1) == 0
assert multiply(0, 0) == 0
