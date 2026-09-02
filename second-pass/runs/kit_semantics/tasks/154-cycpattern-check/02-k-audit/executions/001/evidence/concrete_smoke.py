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
assert cycpattern_check("", "") == True
assert cycpattern_check("abc", "") == True
assert cycpattern_check("", "a") == False
assert cycpattern_check("a", "a") == True
assert cycpattern_check("a", "b") == False
assert cycpattern_check("ba", "ab") == True
assert cycpattern_check("zzbcda", "abcd") == True
assert cycpattern_check("zzdabc", "abcd") == True
assert cycpattern_check("zzcabd", "abcd") == False
