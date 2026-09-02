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
boundary_prime = words_in_sentence("a bb ccc dddd eeeee")
boundary_nonprime = words_in_sentence("abcd")

assert example_1 == "is"
assert example_2 == "go for"
assert boundary_prime == "bb ccc eeeee"
assert boundary_nonprime == ""
