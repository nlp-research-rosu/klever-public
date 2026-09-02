def get_closest_vowel(word):
    result = ""
    p1 = 0
    p2 = 0
    i = 0
    c = ""
    code = 0
    for c in word:
        code = ord(c)
        if i >= 2:
            if (p1 == 97 or p1 == 101 or p1 == 105 or p1 == 111 or p1 == 117 or p1 == 65 or p1 == 69 or p1 == 73 or p1 == 79 or p1 == 85) and (not (p2 == 97 or p2 == 101 or p2 == 105 or p2 == 111 or p2 == 117 or p2 == 65 or p2 == 69 or p2 == 73 or p2 == 79 or p2 == 85)) and (not (code == 97 or code == 101 or code == 105 or code == 111 or code == 117 or code == 65 or code == 69 or code == 73 or code == 79 or code == 85)):
                result = chr(p1)
        p2 = p1
        p1 = code
        i = i + 1
    return result


# HumanEval/118 test cases (the dataset `check`); returns a string.
assert get_closest_vowel("yogurt") == "u"
assert get_closest_vowel("full") == "u"
assert get_closest_vowel("easy") == ""
assert get_closest_vowel("bad") == "a"
assert get_closest_vowel("most") == "o"
assert get_closest_vowel("ab") == ""
assert get_closest_vowel("quick") == ""
assert get_closest_vowel("anime") == "i"
assert get_closest_vowel("Above") == "o"
