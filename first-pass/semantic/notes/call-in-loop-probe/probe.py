def digsum(k):
    s = 0
    while k > 0:
        s = s + k % 10
        k = k // 10
    return s


def total_digsum(n):
    t = 0
    i = 0
    for i in range(n):
        t = t + digsum(i)
    return t


assert total_digsum(0) == 0
assert total_digsum(5) == 10
assert total_digsum(12) == 48
