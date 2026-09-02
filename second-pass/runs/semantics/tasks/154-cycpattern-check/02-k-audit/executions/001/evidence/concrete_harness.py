def cycpattern_check(a, b):
    pattern = b
    char = ""
    for char in b:
        if pattern in a:
            return True
        pattern = pattern[1:] + char
    return False


# Documented examples.
assert cycpattern_check("abcd", "abd") == False
assert cycpattern_check("hello", "ell") == True
assert cycpattern_check("whassup", "psus") == False
assert cycpattern_check("abab", "baa") == True
assert cycpattern_check("efef", "eeff") == False
assert cycpattern_check("himenss", "simen") == True

# Empty and branch-boundary cases for the submitted implementation.
assert cycpattern_check("", "") == False
assert cycpattern_check("a", "") == False
assert cycpattern_check("", "a") == False
assert cycpattern_check("a", "a") == True
assert cycpattern_check("a", "b") == False
assert cycpattern_check("ab", "ba") == True
assert cycpattern_check("ab", "aba") == False
assert cycpattern_check("xxbcayy", "abc") == True
