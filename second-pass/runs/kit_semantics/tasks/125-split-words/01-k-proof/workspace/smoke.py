def split_words(txt):
    parts = txt.split()
    if txt and parts != [txt]:
        return parts
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
        + txt.count("z")
    )


assert split_words("Hello world!") == ["Hello", "world!"]
assert split_words("Hello,world!") == ["Hello", "world!"]
assert split_words("abcdef") == 3
assert split_words("") == 0
assert split_words(",") == ["", ""]
# Reference-model boundary witness: its isWSC table omits vertical tab.
assert split_words("\v") == 0
