def is_happy(s):
    if len(s) < 3:
        return False
    i = 0
    while i + 2 < len(s):
        if s[i] == s[i + 1]:
            return False
        if s[i] == s[i + 2]:
            return False
        if s[i + 1] == s[i + 2]:
            return False
        i += 1
    return True
