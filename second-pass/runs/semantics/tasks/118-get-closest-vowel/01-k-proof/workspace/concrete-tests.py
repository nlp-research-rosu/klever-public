def get_closest_vowel(word):
    if len(word) < 3:
        return ""
    result = get_closest_vowel(word[1:])
    if result:
        return result
    if (
        word[1] in "AEIOUaeiou"
        and word[0] not in "AEIOUaeiou"
        and word[2] not in "AEIOUaeiou"
    ):
        return word[1]
    return ""


assert get_closest_vowel("yogurt") == "u"
assert get_closest_vowel("FULL") == "U"
assert get_closest_vowel("quick") == ""
assert get_closest_vowel("ab") == ""
assert get_closest_vowel("") == ""
assert get_closest_vowel("bab") == "a"
assert get_closest_vowel("xAy") == "A"
assert get_closest_vowel("BAZZE") == "A"
