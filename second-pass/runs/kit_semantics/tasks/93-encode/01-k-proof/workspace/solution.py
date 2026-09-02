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
