def any_int(x, y, z):
    return (
        isinstance(x, int)
        and isinstance(y, int)
        and isinstance(z, int)
        and (x + y == z or x + z == y or y + z == x)
    )


# Documented examples.
assert any_int(5, 2, 7)
assert not any_int(3, 2, 2)
assert any_int(3, -2, 1)
assert not any_int(3.6, -2.2, 2)

# Every integer result branch, zero boundary, negatives, and large integers.
assert any_int(5, 7, 2)
assert any_int(7, 5, 2)
assert any_int(0, 0, 0)
assert not any_int(0, 0, 1)
assert any_int(-5, 2, -3)
assert any_int(100000000000000000000, -100000000000000000000, 0)

# Each non-integer short-circuit position.
assert not any_int(1.0, 2, 3)
assert not any_int(1, 2.0, 3)
assert not any_int(1, 2, 3.0)
