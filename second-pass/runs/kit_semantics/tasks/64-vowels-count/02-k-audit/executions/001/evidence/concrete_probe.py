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
assert vowels_count("a") == 1
assert vowels_count("b") == 0
assert vowels_count("y") == 1
assert vowels_count("Y") == 1
assert vowels_count("ya") == 1
assert vowels_count("ay") == 2
assert vowels_count("rhythm") == 0
assert vowels_count("AEIOU") == 5
assert vowels_count("123y") == 1
