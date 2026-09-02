# Tuple value: literal, == / != (a list never equals a tuple), and unpacking
# in assignment, in a for target, and from a function's multiple return.
t = (1, 2)
assert t == (1, 2)
assert (1, 2) != (1, 3)

a, b = t
assert a == 1
assert b == 2

m, n = 3, 4
assert m + n == 7

# unpack from a list target too
x, y = [5, 6]
assert x == 5 and y == 6

# tuple as a for target
total = 0
for p, q in [(1, 2), (3, 4)]:
    total = total + p * q
assert total == 14

# multiple return is just a returned tuple
def pair():
    return 7, 8


u, v = pair()
assert u == 7
assert v == 8
