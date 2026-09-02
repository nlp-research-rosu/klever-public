def vowels_count(s):
    count = 0
    last = ""
    char = ""
    for char in s:
        count += char in "aeiouAEIOU"
        last = char
    count += last == "y"
    count += last == "Y"
    return count
