def vowels_count(s):
    s = s.lower()
    count = 0
    char = ""
    last_y = False
    for char in s:
        if char in "aeiou":
            count += 1
        last_y = char in "y"
    return count + last_y


assert vowels_count("İ") == 1
