def count_upper(s):
    if len(s) == 0:
        return 0
    if s[0] in "AEIOU":
        return 1 + count_upper(s[2:])
    return count_upper(s[2:])
