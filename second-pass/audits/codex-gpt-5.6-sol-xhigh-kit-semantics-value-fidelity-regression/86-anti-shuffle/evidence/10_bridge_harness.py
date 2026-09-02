x = 0
y = 0

if True:
    x = 1
else:
    x = 2
y = 3
assert x == 1
assert y == 3

if False:
    x = 4
else:
    x = 5
y = 6
assert x == 5
assert y == 6
