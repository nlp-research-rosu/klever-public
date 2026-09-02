def decode_shift(s):
    result = ""
    ch = ""
    for ch in s:
        result = result + chr(((ord(ch) - 5 - 97) % 26) + 97)
    return result
