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
assert string_xor("", "101") == ""
assert string_xor("101", "") == ""
assert string_xor("0", "0") == "0"
assert string_xor("0", "1") == "1"
assert string_xor("1", "0") == "1"
assert string_xor("1", "1") == "0"
assert string_xor("01", "10110") == "11"
assert string_xor("10110", "01") == "11"
assert string_xor("01010101", "10101010") == "11111111"
