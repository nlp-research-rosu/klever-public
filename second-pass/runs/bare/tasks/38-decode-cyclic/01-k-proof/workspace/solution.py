def decode_cyclic(s: str):
    result = ""
    i = 0
    while i + 2 < len(s):
        result = result + s[i + 2] + s[i:i + 2]
        i = i + 3
    return result + s[i:]
