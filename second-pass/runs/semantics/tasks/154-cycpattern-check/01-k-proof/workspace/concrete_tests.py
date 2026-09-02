def cycpattern_check(a, b):
    pattern = b
    char = ""
    for char in b:
        if pattern in a:
            return True
        pattern = pattern[1:] + char
    return False


assert cycpattern_check("abcd", "abd") == False
assert cycpattern_check("hello", "ell") == True
assert cycpattern_check("whassup", "psus") == False
assert cycpattern_check("abab", "baa") == True
assert cycpattern_check("efef", "eeff") == False
assert cycpattern_check("himenss", "simen") == True
assert cycpattern_check("anything", "") == False
