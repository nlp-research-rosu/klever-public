def encode(message):
    result = ""
    for char in message:
        if char in "aeiouAEIOU":
            char = chr(ord(char) + 2)
        result += char.swapcase()
    return result
