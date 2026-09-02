def encode_shift(s: str):
    return "".join([chr(((ord(ch) + 5 - ord("a")) % 26) + ord("a")) for ch in s])


def decode_shift(s: str):
    result = ""
    ch = ""
    for ch in s:
        result += chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))
    return result


assert decode_shift("") == ""
assert decode_shift("mjqqt") == "hello"
assert decode_shift("c") == "x"
assert decode_shift("fghijklmnopqrstuvwxyzabcde") == "abcdefghijklmnopqrstuvwxyz"
