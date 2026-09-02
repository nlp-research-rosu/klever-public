# Assign (x = e) and AugAssign (x OP= e) write the current scope.
x = 5
assert x == 5
x = x + 10
assert x == 15
y = 100
y += 1
assert y == 101
y -= 50
assert y == 51
