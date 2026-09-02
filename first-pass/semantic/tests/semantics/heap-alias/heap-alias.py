a = [1]
b = a
b.append(2)
assert a == [1, 2]
assert b == a


def extend_it(xs):
    xs.append(9)


c = [3, 4]
extend_it(c)
assert c == [3, 4, 9]

d = c + [5]
d.append(6)
assert c == [3, 4, 9]
assert d == [3, 4, 9, 5, 6]
