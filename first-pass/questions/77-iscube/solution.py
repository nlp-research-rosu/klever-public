def iscube(a):
    a = abs(a)
    found = False
    r = 0
    for r in range(0, a + 1):
        if r * r * r == a:
            found = True
    return found
