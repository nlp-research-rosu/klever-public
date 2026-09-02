def fibfib(n: int):
    a = 0
    b = 0
    c = 1
    i = 0
    d = 0
    while i < n:
        d = a + b + c
        a = b
        b = c
        c = d
        i = i + 1
    return a
