def insert_char(char, word, before):
    if word == "":
        return before + char
    if char <= word[0]:
        return before + char + word
    return insert_char(char, word[1:], before + word[0])


def process_words(text, word, result):
    if text == "":
        return result + word
    if text[0] == " ":
        return process_words(text[1:], "", result + word + " ")
    return process_words(
        text[1:], insert_char(text[0], word, ""), result
    )


def anti_shuffle(s):
    return process_words(s, "", "")
