def words_in_sentence(sentence):
    result = ""
    word = ""
    char = ""
    for char in sentence:
        if char == " ":
            if len(word) in (
                2,
                3,
                5,
                7,
                11,
                13,
                17,
                19,
                23,
                29,
                31,
                37,
                41,
                43,
                47,
                53,
                59,
                61,
                67,
                71,
                73,
                79,
                83,
                89,
                97,
            ):
                result = result + word + " "
            word = ""
        else:
            word = word + char
    if len(word) in (
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
    ):
        result = result + word + " "
    return result.strip()


example_1 = words_in_sentence("This is a test")
example_2 = words_in_sentence("lets go for swimming")
minimum = words_in_sentence("a")
prime_two = words_in_sentence("aa")
repeated_spaces = words_in_sentence("aa  bbb    cccc")
maximum_composite = words_in_sentence(
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)

assert example_1 == "is"
assert example_2 == "go for"
assert minimum == ""
assert prime_two == "aa"
assert repeated_spaces == "aa bbb"
assert maximum_composite == ""
