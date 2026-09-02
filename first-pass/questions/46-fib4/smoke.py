def fib4(n):
    if n < 4:
        return 2 if n == 2 else 0
    a, b, c, d = 0, 0, 2, 0
    for _ in range(4, n + 1):
        a, b, c, d = b, c, d, a + b + c + d
    return d


# Smoke checks from the HumanEval/46 `check` cases (+ docstring examples).
assert fib4(5) == 4
assert fib4(6) == 8
assert fib4(7) == 14
assert fib4(8) == 28
assert fib4(10) == 104
assert fib4(12) == 386
