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


# Reviewer-selected cases: documented example, empty and unequal inputs, and
# all equality/inequality branch combinations at a single character.
assert string_xor("010", "110") == "100"
assert string_xor("", "") == ""
assert string_xor("", "1") == ""
assert string_xor("0", "") == ""
assert string_xor("0", "0") == "0"
assert string_xor("1", "1") == "0"
assert string_xor("0", "1") == "1"
assert string_xor("1", "0") == "1"
assert string_xor("10", "1") == "0"
assert string_xor("1", "10") == "0"
assert string_xor("1111", "0101") == "1010"
