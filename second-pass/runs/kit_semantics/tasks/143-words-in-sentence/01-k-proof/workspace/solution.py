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
