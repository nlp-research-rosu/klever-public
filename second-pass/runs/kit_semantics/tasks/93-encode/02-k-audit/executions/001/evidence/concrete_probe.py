#!/usr/bin/env python3


def encode(message):
    return (
        message.swapcase()
        .replace("a", "c")
        .replace("e", "g")
        .replace("i", "k")
        .replace("o", "q")
        .replace("u", "w")
        .replace("A", "C")
        .replace("E", "G")
        .replace("I", "K")
        .replace("O", "Q")
        .replace("U", "W")
    )


assert encode("") == ""
assert encode("test") == "TGST"
assert encode("This is a message") == "tHKS KS C MGSSCGG"
assert encode("aeiouAEIOU") == "CGKQWcgkqw"
assert encode("bcdXYZ z") == "BCDxyz Z"
assert encode("aA eE iI oO uU") == "Cc Gg Kk Qq Ww"
