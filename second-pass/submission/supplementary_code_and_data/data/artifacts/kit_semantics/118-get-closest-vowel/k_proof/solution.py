def _is_vowel(ch):
    result = False
    while ch == "a":
        result = True
        ch = ""
    while ch == "e":
        result = True
        ch = ""
    while ch == "i":
        result = True
        ch = ""
    while ch == "o":
        result = True
        ch = ""
    while ch == "u":
        result = True
        ch = ""
    while ch == "A":
        result = True
        ch = ""
    while ch == "E":
        result = True
        ch = ""
    while ch == "I":
        result = True
        ch = ""
    while ch == "O":
        result = True
        ch = ""
    while ch == "U":
        result = True
        ch = ""
    return result


def get_closest_vowel(word):
    result = ""
    found = False
    i = len(word) - 2
    while i > 0:
        while (not found and _is_vowel(word[i])
               and not _is_vowel(word[i - 1])
               and not _is_vowel(word[i + 1])):
            result = word[i]
            found = True
        i = i - 1
    return result
