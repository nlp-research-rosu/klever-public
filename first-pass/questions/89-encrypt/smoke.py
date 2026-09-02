def encrypt(s):
    out = ""
    c = ""
    code = 0
    new = 0
    for c in s:
        code = ord(c)
        new = code
        if code >= 97 and code <= 122:
            new = (code - 97 + 4) % 26 + 97
        out = out + chr(new)
    return out


# HumanEval/89 test cases (the dataset `check`); returns a string.
assert encrypt("hi") == "lm"
assert encrypt("asdfghjkl") == "ewhjklnop"
assert encrypt("gf") == "kj"
assert encrypt("et") == "ix"
assert encrypt("faewfawefaewg") == "jeiajeaijeiak"
assert encrypt("hellomyfriend") == "lippsqcjvmirh"
assert encrypt("a") == "e"
