def cycpattern_check(a, b):
    """Return whether b or one of its rotations is a substring of a."""
    result = b in a
    rotation = b
    c = ""
    for c in b[:-1]:
        rotation = rotation[1:] + c
        result = result or rotation in a
    return result
