def encode(message):
    result = ""
    c = ""
    code = 0
    new = 0
    for c in message:
        code = ord(c)
        new = code
        if code >= 65 and code <= 90:
            new = code + 32
        elif code >= 97 and code <= 122:
            new = code - 32
        if new == 97 or new == 101 or new == 105 or new == 111 or new == 117 or new == 65 or new == 69 or new == 73 or new == 79 or new == 85:
            new = new + 2
        result = result + chr(new)
    return result
