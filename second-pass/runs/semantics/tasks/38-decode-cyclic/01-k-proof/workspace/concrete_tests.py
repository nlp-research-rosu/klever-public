def encode_cyclic(s: str):
    """
    returns encoded string by cycling groups of three characters.
    """
    # split string to groups. Each of length 3.
    groups = [s[(3 * i):min((3 * i + 3), len(s))] for i in range((len(s) + 2) // 3)]
    # cycle elements in each group. Unless group has fewer elements than 3.
    groups = [(group[1:] + group[0]) if len(group) == 3 else group for group in groups]
    return "".join(groups)


def decode_cyclic(s: str):
    """
    takes as input string encoded with encode_cyclic function. Returns decoded string.
    """
    if len(s) < 3:
        return s
    return s[2] + s[:2] + decode_cyclic(s[3:])


assert decode_cyclic("") == ""
assert decode_cyclic("a") == "a"
assert decode_cyclic("ab") == "ab"
assert decode_cyclic("bca") == "abc"
assert decode_cyclic("bcaefd") == "abcdef"
assert decode_cyclic("bcaefdg") == "abcdefg"
assert decode_cyclic("elho lorwld") == "hello world"
assert decode_cyclic(encode_cyclic("0123456789")) == "0123456789"
