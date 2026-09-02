def any_int(x, y, z):
    return (
        isinstance(x, int)
        and isinstance(y, int)
        and isinstance(z, int)
        and (x + y == z or x + z == y or y + z == x)
    )


assert any_int(5, 2, 7)
assert not any_int(3, 2, 2)
assert any_int(3, -2, 1)
assert not any_int(3.6, -2.2, 2)
assert any_int(7, 5, 2)
assert any_int(-5, 2, -3)
assert not any_int(0, 0, 1)
