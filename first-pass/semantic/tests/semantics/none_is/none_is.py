# None value + `is` / `is not` (modeled only against None). None is falsy, so `not
# None` is True. None flows through assignment, return, and condition positions.
a = None
assert a is None
assert (a is not None) == False

b = 5
assert b is not None
assert (b is None) == False
assert not None


def f(x):
    if x is None:
        return -1
    return x


assert f(None) == -1
assert f(7) == 7
