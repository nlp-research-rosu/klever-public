def iscube(a):
    if a < 0:
        a = -a

    candidate = 0
    while candidate * candidate * candidate < a:
        candidate += 1

    return candidate * candidate * candidate == a


# Prompt examples.
assert iscube(1) == True
assert iscube(2) == False
assert iscube(-1) == True
assert iscube(64) == True
assert iscube(0) == True
assert iscube(180) == False

# Independent sign, loop-entry, exact-hit, and just-above/below boundaries.
assert iscube(-65) == False
assert iscube(-64) == True
assert iscube(-63) == False
assert iscube(-2) == False
assert iscube(7) == False
assert iscube(8) == True
assert iscube(9) == False
assert iscube(26) == False
assert iscube(27) == True
assert iscube(28) == False
