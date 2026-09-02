def fib4(n: int):
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n == 2:
        return 2
    if n == 3:
        return 0

    a = 0
    b = 0
    c = 2
    d = 0
    e = 0
    i = 4
    while i <= n:
        e = a + b + c + d
        a = b
        b = c
        c = d
        d = e
        i = i + 1
    return d
