def cycpattern_check(a, b):
    pattern = b
    char = ""
    for char in b:
        if pattern in a:
            return True
        pattern = pattern[1:] + char
    return False
