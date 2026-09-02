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
