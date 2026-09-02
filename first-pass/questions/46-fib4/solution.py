def fib4(n):
    if n < 4:
        return 2 if n == 2 else 0
    a, b, c, d = 0, 0, 2, 0
    for _ in range(4, n + 1):
        a, b, c, d = b, c, d, a + b + c + d
    return d
