def encrypt(s):
    if s == "":
        return ""
    return chr((ord(s[0]) - 97 + 4) % 26 + 97) + encrypt(s[1:])
