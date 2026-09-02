def any_int(x, y, z):
    return (
        type(x) == int
        and type(y) == int
        and type(z) == int
        and (x + y == z or x + z == y or y + z == x)
    )
