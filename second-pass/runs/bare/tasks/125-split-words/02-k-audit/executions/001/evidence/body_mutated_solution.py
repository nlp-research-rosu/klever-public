def split_words(txt):
    words = txt.split()
    if "".join(words) != txt:
        return words
    if "," in txt:
        return txt.split(",")
    return (
        txt.count("b")
        + txt.count("d")
        + txt.count("f")
        + txt.count("h")
        + txt.count("j")
        + txt.count("l")
        + txt.count("n")
        + txt.count("p")
        + txt.count("r")
        + txt.count("t")
        + txt.count("v")
        + txt.count("x")
        + txt.count("a")
    )
