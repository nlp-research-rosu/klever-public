def fib(n: int):
    a = 0
    b = 1
    while n > 0:
        b = a + b
        a = b - a
        n = n - 1
    return a


assert fib(0) == 0
assert fib(1) == 1
assert fib(2) == 1
assert fib(8) == 21
assert fib(10) == 55
