def remove_vowels(text):
    result = ""
    char = ""
    for char in text:
        if char not in "aeiouAEIOU":
            result += char
    return result


assert remove_vowels("") == ""
assert remove_vowels("abcdef\nghijklm") == "bcdf\nghjklm"
assert remove_vowels("abcdef") == "bcdf"
assert remove_vowels("aaaaa") == ""
assert remove_vowels("aaBAA") == "B"
assert remove_vowels("zbcd") == "zbcd"
