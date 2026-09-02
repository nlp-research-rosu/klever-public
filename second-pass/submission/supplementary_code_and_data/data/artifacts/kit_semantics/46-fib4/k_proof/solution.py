def fib4(n: int):
    a = 0
    b = 0
    c = 2
    d = 0
    e = 0
    i = 0

    while i < n:
        e = a + b + c + d
        a = b
        b = c
        c = d
        d = e
        i = i + 1

    return a
