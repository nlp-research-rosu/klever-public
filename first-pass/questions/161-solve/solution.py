def solve(s):
    has_alpha = False
    swapped = ""
    rev = ""
    c = ""
    code = 0
    new = 0
    for c in s:
        code = ord(c)
        new = code
        if code >= 65 and code <= 90:
            new = code + 32
            has_alpha = True
        elif code >= 97 and code <= 122:
            new = code - 32
            has_alpha = True
        swapped = swapped + chr(new)
        rev = c + rev
    result = rev
    if has_alpha:
        result = swapped
    return result
