def encode(message):
    result = ""
    for c in message:
        if c in "aeiouAEIOU":
            c = chr(ord(c) + 2)
        result += c.swapcase()
    return result
