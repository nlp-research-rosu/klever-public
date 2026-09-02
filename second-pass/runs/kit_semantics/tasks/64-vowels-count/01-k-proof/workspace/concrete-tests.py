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


assert vowels_count("") == 0
assert vowels_count("abcde") == 2
assert vowels_count("ACEDY") == 3
assert vowels_count("yyy") == 1
assert vowels_count("rhythm") == 0
assert vowels_count("AEIOU") == 5
assert vowels_count("sky") == 1
assert vowels_count("yellow") == 2
