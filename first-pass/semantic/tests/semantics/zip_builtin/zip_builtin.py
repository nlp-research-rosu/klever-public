# zip(a, b): parallel iteration, truncating to the shorter list
r = []
for x, y in zip([1, 2, 3], [10, 20, 30]):
    r = r + [x + y]
assert r == [11, 22, 33]

# truncates to the shorter
r2 = []
for x, y in zip([1, 2, 3, 4], [10, 20]):
    r2 = r2 + [x + y]
assert r2 == [11, 22]

# empty
r3 = []
for x, y in zip([], [1, 2]):
    r3 = r3 + [x]
assert r3 == []

# zip over two strings yields pairs of 1-char strings
rs = ""
for x, y in zip("abc", "xyz"):
    if x == y:
        rs = rs + "="
    else:
        rs = rs + "!"
assert rs == "!!!"
