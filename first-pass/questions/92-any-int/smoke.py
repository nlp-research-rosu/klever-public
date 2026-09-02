def any_int(x, y, z):
    if isinstance(x, int) and isinstance(y, int) and isinstance(z, int):
        if x + y == z or x + z == y or y + z == x:
            return True
        return False
    return False


# Smoke checks from the prompt docstring (NOT hidden tests).
assert any_int(5, 2, 7) == True
assert any_int(3, 2, 2) == False
assert any_int(3, 4, 7) == True
assert any_int(2, 2, 2) == False
