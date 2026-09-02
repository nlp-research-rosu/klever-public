# BoolOp: short-circuit, value-returning `and` / `or` (variadic). Bool operands here;
# `and` returns the first falsy operand (else the last), `or` the first truthy (else
# the last). Short-circuit means a falsy `and` / truthy `or` never evaluates the rest.
assert (True and True) == True
assert (True and False) == False
assert (False and True) == False
assert (False or True) == True
assert (False or False) == False
assert (True or False) == True

# operands are themselves comparisons
assert (1 < 2 and 3 < 4) == True
assert (1 > 2 or 3 < 4) == True

# variadic (three operands)
assert (True and True and False) == False
assert (False or False or True) == True

# short-circuit: a falsy `and` / truthy `or` must NOT touch the rest. `_unreached` is
# never defined; evaluating it would be a NameError, so reaching it fails the test.
assert (False and _unreached) == False
assert (True or _unreached) == True
