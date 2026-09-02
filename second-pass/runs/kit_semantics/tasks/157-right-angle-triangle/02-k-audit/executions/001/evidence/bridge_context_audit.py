# The candidate bridge accepts arbitrary continuations after an evaluated
# Float/Float equality.  These assignments make that continuation observable.
x = 0
if 1.0 == 1.0:
    x = 11
else:
    x = 12
assert x == 11

y = 0
if 1.0 == 2.0:
    y = 21
else:
    y = 22
assert y == 22

# Also exercise both outcomes beneath the BoolOp/Return-like expression shape.
assert (3.0 == 3.0 or False) == True
assert (3.0 == 4.0 or False) == False
