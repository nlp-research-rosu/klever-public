def cycpattern_check(a, b):
    i = 0
    while i < len(b):
        if b[i:] + b[:i] in a:
            # Audit mutation: change a successful match's returned value.
            return False
        i = i + 1
    return False
