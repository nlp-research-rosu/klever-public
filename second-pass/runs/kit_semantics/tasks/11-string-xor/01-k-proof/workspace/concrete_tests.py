def string_xor(a: str, b: str) -> str:
    result = ""
    x = ""
    y = ""
    for x, y in zip(a, b):
        if x == y:
            result += "0"
        else:
            result += "1"
    return result


assert string_xor("010", "110") == "100"
assert string_xor("", "") == ""
assert string_xor("1", "0") == "1"
assert string_xor("1011", "01") == "11"
