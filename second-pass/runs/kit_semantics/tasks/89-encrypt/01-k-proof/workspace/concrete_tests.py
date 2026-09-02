def encrypt(s):
    """Rotate lowercase letters four places and preserve other characters."""
    out = ""
    c = ""
    for c in s:
        if ord(c) >= 97 and ord(c) <= 122:
            out += chr((ord(c) - 97 + 4) % 26 + 97)
        else:
            out += c
    return out


assert encrypt("hi") == "lm"
assert encrypt("asdfghjkl") == "ewhjklnop"
assert encrypt("gf") == "kj"
assert encrypt("et") == "ix"
assert encrypt("") == ""
assert encrypt("xyz") == "bcd"
assert encrypt("a z!") == "e d!"
