def fib(n: int):
    a = 0
    b = 1
    while n > 0:
        b = a + b
        a = b - a
        n = n - 1
    return a
