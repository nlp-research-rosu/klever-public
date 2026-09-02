def fibfib(n: int):
    a = 0
    b = 0
    c = 1
    i = 0
    next_value = 1
    while i < n:
        next_value = a + b + c
        a = b
        b = c
        c = next_value
        i = i + 1
    return a
