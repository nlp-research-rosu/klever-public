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
