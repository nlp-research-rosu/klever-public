def any_int(x, y, z):
    return (
        isinstance(x, int)
        and isinstance(y, int)
        and isinstance(z, int)
        and (x + y == z or x + z == y or y + z == x)
    )


# Prompt examples.
assert any_int(5, 2, 7) == True
assert any_int(3, 2, 2) == False
assert any_int(3, -2, 1) == True
assert any_int(3.6, -2.2, 2) == False

# Zero, negative, large, and each equality branch.
assert any_int(0, 0, 0) == True
assert any_int(-7, 3, -4) == True
assert any_int(4, 13, 9) == True
assert any_int(13, 4, 9) == True
assert any_int(10000000000000000000000000000000000000000, 1, 10000000000000000000000000000000000000001) == True
assert any_int(4, 9, 14) == False

# CPython Bool-as-int boundaries and float rejection at each position.
assert any_int(True, True, 2) == True
assert any_int(False, False, False) == True
assert any_int(True, False, False) == False
assert any_int(1.0, 1, 2) == False
assert any_int(1, 1.0, 2) == False
assert any_int(1, 2, 3.0) == False
