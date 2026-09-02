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


result_empty = vowels_count("")
result_a = vowels_count("a")
result_y = vowels_count("y")
result_by = vowels_count("by")
result_abcde = vowels_count("abcde")
result_acedy = vowels_count("ACEDY")
result_yellowy = vowels_count("yellowy")
