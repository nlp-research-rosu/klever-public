def solve(N):
    s = 0
    while N > 0:
        s = s + N % 10
        N = N // 10
    if s == 0:
        return '0'
    ret = ''
    while s > 0:
        ret = str(s % 2) + ret
        s = s // 2
    return ret


# Smoke checks from the prompt docstring (NOT hidden tests).
assert solve(1000) == "1"
assert solve(150) == "110"
assert solve(147) == "1100"
assert solve(0) == "0"
assert solve(9999) == "100100"
