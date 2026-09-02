t = (1, 2, 3, 2)
assert 2 in t
assert 5 not in t
assert t.index(2) == 1
assert t.index(3) == 2
assert t[1:3] == (2, 3)
assert t[:2] == (1, 2)
assert t[2:] == (3, 2)
u = ("a", "b")
assert "a" in u
assert u.index("b") == 1
