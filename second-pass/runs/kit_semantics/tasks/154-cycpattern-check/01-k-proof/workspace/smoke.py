def cycpattern_check(a, b):
    """Return whether b or one of its rotations is a substring of a."""
    result = b in a
    rotation = b
    c = ""
    for c in b[:-1]:
        rotation = rotation[1:] + c
        result = result or rotation in a
    return result


assert cycpattern_check("abcd", "abd") == False
assert cycpattern_check("hello", "ell") == True
assert cycpattern_check("whassup", "psus") == False
assert cycpattern_check("abab", "baa") == True
assert cycpattern_check("efef", "eeff") == False
assert cycpattern_check("himenss", "simen") == True
assert cycpattern_check("abc", "") == True
