def decode_shift(s: str):
    result = ""
    ch = ""
    for ch in s:
        result = result + chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))
    return result


assert decode_shift("") == ""
assert decode_shift("fghij") == "abcde"
assert decode_shift("c") == "x"
assert decode_shift("fghijklmnopqrstuvwxyzabcde") == "abcdefghijklmnopqrstuvwxyz"
