def encrypt(s):
    result = ""
    char = ""
    for char in s:
        result += chr((ord(char) - 97 + 4) % 26 + 97)
    return result


assert encrypt("") == ""
assert encrypt("hi") == "lm"
assert encrypt("wxyz") == "abcd"
assert encrypt("A") == "y"
assert encrypt("aZ-9z") == "exeqd"
