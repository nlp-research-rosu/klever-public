def any_int(x, y, z):
    return (
        isinstance(x, int)
        and isinstance(y, int)
        and isinstance(z, int)
        and (x + y == z or x + z == y or y + z == x)
    )


# The trusted K semantics defines isIntV(Bool) as false.
assert not any_int(True, False, True)
