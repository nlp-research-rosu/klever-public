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


assert encode("test") == "TGST"
assert encode("This is a message") == "tHKS KS C MGSSCGG"
assert encode("aeiouAEIOU") == "CGKQWcgkqw"
assert encode("xyz XYZ") == "XYZ xyz"
assert encode("") == ""
