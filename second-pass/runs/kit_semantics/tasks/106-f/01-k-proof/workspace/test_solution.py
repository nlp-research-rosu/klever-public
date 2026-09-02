import math

from solution import f


def oracle(n):
    return [
        math.factorial(i) if i % 2 == 0 else sum(range(1, i + 1))
        for i in range(1, n + 1)
    ]


for value in range(0, 51):
    assert f(value) == oracle(value), (value, f(value), oracle(value))

print("51 cases, 0 mismatches")
