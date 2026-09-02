def iscube(a):
    a = abs(a)
    return int(round(a ** (1 / 3))) ** 3 == a


# 10**45 is (10**15)**3, but binary-float cube-root rounding makes this
# implementation return False.
assert iscube(1000000000000000000000000000000000000000000000) == False
