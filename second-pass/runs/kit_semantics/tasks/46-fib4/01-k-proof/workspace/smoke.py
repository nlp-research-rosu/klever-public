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


assert fib4(0) == 0
assert fib4(1) == 0
assert fib4(2) == 2
assert fib4(3) == 0
assert fib4(5) == 4
assert fib4(6) == 8
assert fib4(7) == 14
assert fib4(10) == 104
