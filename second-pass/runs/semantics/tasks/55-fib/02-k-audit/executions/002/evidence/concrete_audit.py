def fib(n: int):
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
    a = 0
    b = 1
    _ = 0
    for _ in range(n):
        a, b = b, a + b
    return a


assert fib(0) == 0
assert fib(1) == 1
assert fib(2) == 1
assert fib(8) == 21
assert fib(10) == 55
assert fib(30) == 832040
