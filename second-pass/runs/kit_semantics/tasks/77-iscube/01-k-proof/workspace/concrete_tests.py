def iscube(a):
    if a < 0:
        a = -a

    candidate = 0
    while candidate * candidate * candidate < a:
        candidate += 1

    return candidate * candidate * candidate == a


assert iscube(1) == True
assert iscube(2) == False
assert iscube(-1) == True
assert iscube(64) == True
assert iscube(0) == True
assert iscube(180) == False
assert iscube(-64) == True
assert iscube(-2) == False
assert iscube(8) == True
assert iscube(27) == True
