def iscube(a):
    a = abs(a)
    return int(round(a ** (1 / 3))) ** 3 == a


# 10^45 is exactly (10^15)^3. CPython returns False because the floating
# cube-root approximation rounds to the wrong integer.
iscube(1000000000000000000000000000000000000000000000)
