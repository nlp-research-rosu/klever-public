def decode_shift(s: str):
    """
    takes as input string encoded with encode_shift function. Returns decoded string.
    """
    result = ""
    ch = ""
    for ch in s:
        result = result + chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))
    return result


assert decode_shift("") == ""
assert decode_shift("a") == "v"
assert decode_shift("e") == "z"
assert decode_shift("f") == "a"
assert decode_shift("z") == "u"
assert decode_shift("fghij") == "abcde"
assert decode_shift("abcdefghijklmnopqrstuvwxyz") == "vwxyzabcdefghijklmnopqrstu"
