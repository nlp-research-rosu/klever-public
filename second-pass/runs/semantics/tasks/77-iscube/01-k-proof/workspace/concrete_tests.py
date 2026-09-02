def iscube(a):
    a = abs(a)
    return int(round(a ** (1 / 3))) ** 3 == a


assert iscube(1) == True
assert iscube(2) == False
assert iscube(-1) == True
assert iscube(64) == True
assert iscube(0) == True
assert iscube(180) == False
assert iscube(-125) == True
assert iscube(216) == True
assert iscube(217) == False
