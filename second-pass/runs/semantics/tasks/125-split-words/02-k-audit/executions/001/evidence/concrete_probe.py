def split_words(txt):
    whitespace_count = (
        txt.count(" ")
        + txt.count("\t")
        + txt.count("\n")
        + txt.count("\r")
    )
    if whitespace_count > 0:
        return txt.split()

    if txt.count(",") > 0:
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
assert split_words("a\tb") == ["a", "b"]
assert split_words("a\nb") == ["a", "b"]
assert split_words("a\rb") == ["a", "b"]
assert split_words(",") == ["", ""]
assert split_words(",a") == ["", "a"]
assert split_words("a,") == ["a", ""]
assert split_words("a,,b") == ["a", "", "b"]
assert split_words("Bdfz!") == 3
