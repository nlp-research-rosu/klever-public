def fibfib(n: int):
    a = 0
    b = 0
    c = 1
    i = 0
    while i < n:
        a, b, c = b, c, a + b + c
        i = i + 1
    return b
