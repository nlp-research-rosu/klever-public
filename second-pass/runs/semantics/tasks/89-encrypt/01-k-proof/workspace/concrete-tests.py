def encrypt(s):
    result = ""
    char = ""
    for char in s:
        result += chr((ord(char) - 97 + 4) % 26 + 97)
    return result


assert encrypt("hi") == "lm"
assert encrypt("asdfghjkl") == "ewhjklnop"
assert encrypt("gf") == "kj"
assert encrypt("et") == "ix"
assert encrypt("") == ""
assert encrypt("wxyz") == "abcd"
assert encrypt("abcdefghijklmnopqrstuvwxyz") == "efghijklmnopqrstuvwxyzabcd"
