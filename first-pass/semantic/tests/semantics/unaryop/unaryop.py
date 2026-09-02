# UnaryOp: unary minus / negative integer literals (-4 = UnaryOp("-", Int(4))).
assert -5 < 0
assert -7 < -3
assert -0 == 0

# `not` collapses any operand to a Bool (here Bool / comparison-result / None operands).
assert (not True) == False
assert (not False) == True
assert (not (1 < 2)) == False
assert not None
