def iscube(a):
    a = abs(a)
    found = False
    r = 0
    for r in range(0, a + 1):
        if r * r * r == a:
            found = True
    return found


# HumanEval/77 dataset `check` cases (small |a| only — large a is impractical for krun).
assert iscube(1)
assert not iscube(2)
assert iscube(-1)
assert iscube(64)
assert iscube(0)
assert iscube(8)
assert iscube(27)
assert not iscube(9)
