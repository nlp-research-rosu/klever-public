# solution.py — prime_fib with the sliding-pair fib (canonical's f[-1]/f[-2]
# as scalars) and is_prime as the no-early-exit trial-division accumulator
# (the P139 shape; canonical gap: early return -> accumulator, diff-tested).


def is_prime(p):
    if p < 2:
        return False
    pr = True
    k = 2
    while k * k <= p:
        if p % k == 0:
            pr = False
        k = k + 1
    return pr


def prime_fib(n):
    a = 0
    b = 1
    c = 0
    while n > 0:
        c = a + b
        a = b
        b = c
        if is_prime(c):
            n = n - 1
    return b
