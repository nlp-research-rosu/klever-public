def remove_vowels(text):
    result = ""
    char = ""
    for char in text:
        if char not in "aeiouAEIOU":
            result += char
    return result
