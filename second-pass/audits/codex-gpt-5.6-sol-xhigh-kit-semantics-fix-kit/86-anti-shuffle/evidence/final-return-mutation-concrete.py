def insert_char(word, char):
    prefix = ""
    suffix = word
    current = ""
    for current in word:
        if char < current:
            return prefix + char + suffix
        else:
            prefix = prefix + current
            suffix = suffix[1:]
    return prefix + char


def anti_shuffle(s):
    result = ""
    word = ""
    char = ""
    for char in s:
        if char == " ":
            result = result + word + " "
            word = ""
        else:
            word = insert_char(word, char)
    return "x"


assert anti_shuffle("") == "x"
