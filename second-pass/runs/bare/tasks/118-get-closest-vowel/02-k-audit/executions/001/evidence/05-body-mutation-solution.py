def get_closest_vowel(word):
    vowels = ""
    if len(word) < 3:
        return ""
    if word[-2] in vowels:
        if word[-3] not in vowels:
            if word[-1] not in vowels:
                return word[-2]
    return get_closest_vowel(word[:-1])
