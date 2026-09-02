def any_int(x, y, z):
    return (
        isinstance(x, int)
        and isinstance(y, int)
        and isinstance(z, int)
        and (x + y == z or x + z == y or y + z == x)
    )


# A complex number is inside Python's broad numeric universe, but the fixed
# translator/semantics have no complex value constructor. CPython canonical and
# submitted code both faithfully reject it because it is not an int.
assert any_int(1 + 0j, 1, 2) == False
