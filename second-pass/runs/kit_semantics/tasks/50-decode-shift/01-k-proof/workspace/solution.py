def decode_shift(s: str):
    """
    takes as input string encoded with encode_shift function. Returns decoded string.
    """
    result = ""
    ch = ""
    for ch in s:
        result = result + chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))
    return result
