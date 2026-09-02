def cycpattern_check(a, b):
    i = 0
    while i < len(b):
        if b[i:] + b[:i] in a:
            return True
        i = i + 1
    return False
