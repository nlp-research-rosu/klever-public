# FuncDef / Call / Return — closures, multiple params, and early return (the <ret>
# model: a return records the value and skips the rest of the frame's body).
def inc(n):
    return n + 1


def sub(a, b):
    return a - b


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


assert inc(4) == 5
assert sub(10, 3) == 7
assert sign(5) == 1
assert sign(-2) == -1
assert sign(0) == 0
