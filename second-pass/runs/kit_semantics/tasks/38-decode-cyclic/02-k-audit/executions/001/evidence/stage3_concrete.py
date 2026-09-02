def decode_cyclic(s: str):
    """
    Takes a string encoded by rotating each complete three-character group
    left once, and restores the original string.
    """
    result = ""
    group = ""
    char = ""
    for char in s:
        group = group + char
        if len(group) == 3:
            result = result + (group[2] + group[:2])
            group = ""
    return result + group


assert decode_cyclic("") == ""
assert decode_cyclic("a") == "a"
assert decode_cyclic("ab") == "ab"
assert decode_cyclic("abc") == "cab"
assert decode_cyclic("abcd") == "cabd"
assert decode_cyclic("abcde") == "cabde"
assert decode_cyclic("abcdef") == "cabfde"
assert decode_cyclic("abcdefg") == "cabfdeg"
assert decode_cyclic("abcdefgh") == "cabfdegh"
assert decode_cyclic("abcdefghi") == "cabfdeigh"
assert decode_cyclic("bca") == "abc"
assert decode_cyclic("bcaefdhig") == "abcdefghi"
