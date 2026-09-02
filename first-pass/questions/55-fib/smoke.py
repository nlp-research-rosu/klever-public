def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# Smoke checks from the HumanEval/55 `check` cases.
assert fib(10) == 55
assert fib(1) == 1
assert fib(8) == 21
assert fib(11) == 89
assert fib(12) == 144
