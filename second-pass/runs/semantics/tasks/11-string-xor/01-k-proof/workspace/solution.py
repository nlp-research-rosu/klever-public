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
