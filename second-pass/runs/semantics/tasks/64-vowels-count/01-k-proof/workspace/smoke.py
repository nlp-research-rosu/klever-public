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


assert vowels_count("abcde") == 2
assert vowels_count("ACEDY") == 3
assert vowels_count("") == 0
assert vowels_count("Y") == 1
assert vowels_count("rhythm") == 0
assert vowels_count("AEIOU") == 5
assert vowels_count("yellowy") == 3
