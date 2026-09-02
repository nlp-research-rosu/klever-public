def encode(message):
    result = ""
    char = ""
    code = 0
    for char in message:
        char = char.swapcase()
        code = ord(char)
        if code == 97 or code == 101 or code == 105 or code == 111 or code == 117 or code == 65 or code == 69 or code == 73 or code == 79 or code == 85:
            result += chr(code + 2)
        else:
            result += char
    return result


assert encode("") == ""
assert encode("test") == "TGST"
assert encode("This is a message") == "tHKS KS C MGSSCGG"
assert encode("aeiouAEIOU") == "CGKQWcgkqw"
assert encode("xyz XYZ") == "XYZ xyz"
