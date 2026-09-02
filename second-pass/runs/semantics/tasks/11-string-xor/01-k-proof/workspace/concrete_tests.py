from typing import List


def string_xor(a: str, b: str) -> str:
    """Return the bitwise XOR of two binary strings."""
    result = ""
    x = ""
    y = ""
    for x, y in zip(a, b):
        if x == y:
            result = result + "0"
        else:
            result = result + "1"
    return result


assert string_xor("010", "110") == "100"
assert string_xor("", "") == ""
assert string_xor("1111", "0101") == "1010"
assert string_xor("10", "1") == "0"
