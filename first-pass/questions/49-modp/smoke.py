def modp(n, p):
    ret = 1
    for i in range(n):
        ret = 2 * ret % p
    return ret


# Smoke checks from the prompt docstring (NOT hidden tests).
assert modp(3, 5) == 3
assert modp(1101, 101) == 2
assert modp(0, 101) == 1
assert modp(3, 11) == 8
assert modp(100, 101) == 1
