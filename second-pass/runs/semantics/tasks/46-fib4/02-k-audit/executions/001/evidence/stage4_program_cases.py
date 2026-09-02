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
    next_value = 0
    i = 4
    while i <= n:
        next_value = a + b + c + d
        a = b
        b = c
        c = d
        d = next_value
        i = i + 1
    return d


# Base boundary, zero-iteration/one-iteration loop boundary, and largest
# finite input that the candidate's operational-cases claim mentions.
assert fib4(0) == 0
assert fib4(3) == 0
assert fib4(4) == 2
assert fib4(12) == 386
