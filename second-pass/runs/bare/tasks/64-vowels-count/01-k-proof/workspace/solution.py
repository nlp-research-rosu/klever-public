def vowels_count(s):
    if s == "":
        return 0
    if s[0] in "aeiouAEIOU":
        return 1 + vowels_count(s[1:])
    if len(s) == 1 and s[0] in "yY":
        return 1
    return vowels_count(s[1:])
