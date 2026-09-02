def iscube(a):
    a = abs(a)
    return int(round(a ** (1 / 3))) ** 3 == a


assert iscube(1000000000000000000000000000000000000000000000) == True
