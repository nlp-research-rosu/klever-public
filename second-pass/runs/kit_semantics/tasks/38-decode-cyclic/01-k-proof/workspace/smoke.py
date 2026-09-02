def decode_cyclic(s: str):
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
assert decode_cyclic("bca") == "abc"
assert decode_cyclic("bcaefdhig") == "abcdefghi"
assert decode_cyclic("bcaefdx") == "abcdefx"
