def remove_vowels(text):
    result = ""
    char = ""
    for char in text:
        if char not in "aeiouAEIOU":
            result += char
    return result


# Satisfying entry states and both loop branches.
assert remove_vowels("") == ""
assert remove_vowels("a") == ""
assert remove_vowels("b") == "b"
assert remove_vowels("aeiouAEIOU") == ""
assert remove_vowels("bAeiOUz") == "bz"
assert remove_vowels("abcdef\nghijklm") == "bcdf\nghjklm"
