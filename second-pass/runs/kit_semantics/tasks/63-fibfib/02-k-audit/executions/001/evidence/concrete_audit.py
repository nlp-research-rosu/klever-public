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


# Lower boundary, all base cases, first recurrence transition, and examples.
assert fibfib(0) == 0
assert fibfib(1) == 0
assert fibfib(2) == 1
assert fibfib(3) == 1
assert fibfib(5) == 4
assert fibfib(8) == 24
