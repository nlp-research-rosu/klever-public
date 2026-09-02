def remove_vowels(text):
    result = ""
    char = ""
    for char in text:
        if char not in "aeiouAEIOU":
            result += char
    return result


# These ground the entry claim at empty, vowel-head, and non-vowel-head states.
assert remove_vowels("") == ""
assert remove_vowels("a") == ""
assert remove_vowels("b") == "b"
assert remove_vowels("abEcdU") == "bcd"
