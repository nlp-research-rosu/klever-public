def any_int(x, y, z):
    return (
        isinstance(x, int)
        and isinstance(y, int)
        and isinstance(z, int)
        and (x + y == z or x + z == y or y + z == x)
    )


# The supplied K semantics treats Bool as non-Int.  This assertion therefore
# succeeds in K, while this same Python source assertion is false.
assert not any_int(True, 1, 2)
