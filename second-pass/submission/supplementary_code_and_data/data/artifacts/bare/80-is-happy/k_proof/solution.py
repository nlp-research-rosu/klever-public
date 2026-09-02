def is_happy(s):
    if len(s) < 3:
        return False
    return check_happy_triples(s)


def check_happy_triples(s):
    if len(s) < 3:
        return True
    if s[0] == s[1]:
        return False
    if s[0] == s[2]:
        return False
    if s[1] == s[2]:
        return False
    return check_happy_triples(s[1:])
