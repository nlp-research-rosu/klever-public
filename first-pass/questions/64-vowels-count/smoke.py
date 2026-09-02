def vowels_count(s):
    count = 0
    last = 0
    c = ""
    code = 0
    for c in s:
        code = ord(c)
        if code == 97 or code == 101 or code == 105 or code == 111 or code == 117 or code == 65 or code == 69 or code == 73 or code == 79 or code == 85:
            count = count + 1
        last = code
    if last == 121 or last == 89:
        count = count + 1
    return count


# HumanEval/64 test cases (the dataset `check`); returns an int.
assert vowels_count("abcde") == 2
assert vowels_count("Alone") == 3
assert vowels_count("key") == 2
assert vowels_count("bye") == 1
assert vowels_count("keY") == 2
assert vowels_count("bYe") == 1
assert vowels_count("ACEDY") == 3
