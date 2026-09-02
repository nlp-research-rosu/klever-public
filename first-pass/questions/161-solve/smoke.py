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


# HumanEval/161 test cases (the dataset `check`); returns a string.
assert solve("AsDf") == "aSdF"
assert solve("1234") == "4321"
assert solve("ab") == "AB"
assert solve("#a@C") == "#A@c"
assert solve("#AsdfW^45") == "#aSDFw^45"
assert solve("#6@2") == "2@6#"
assert solve("#$a^D") == "#$A^d"
assert solve("#ccc") == "#CCC"
