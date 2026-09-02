def encrypt(s):
    result = ""
    char = ""
    for char in s:
        result += chr((ord(char) - 97 + 4) % 26 + 97)
    return result
