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
