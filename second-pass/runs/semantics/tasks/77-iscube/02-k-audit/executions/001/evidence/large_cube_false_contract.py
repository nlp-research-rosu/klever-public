def iscube(a):
    a = abs(a)
    return int(round(a ** (1 / 3))) ** 3 == a


# This is the natural exact-cube obligation and the K positive-cubes claim's
# instantiated conclusion. It is false for the actual generated program.
assert iscube(1000000000000000000000000000000000000000000000) == True
