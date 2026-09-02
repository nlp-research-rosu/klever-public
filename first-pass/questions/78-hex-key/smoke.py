def hex_key(num):
    count = 0
    c = ""
    code = 0
    for c in num:
        code = ord(c)
        if code == 50 or code == 51 or code == 53 or code == 55 or code == 66 or code == 68:
            count = count + 1
    return count


# HumanEval/78 test cases (the dataset `check`); returns an int.
assert hex_key("AB") == 1
assert hex_key("1077E") == 2
assert hex_key("ABED1A33") == 4
assert hex_key("2020") == 2
assert hex_key("123456789ABCDEF0") == 6
assert hex_key("112233445566778899AABBCCDDEEFF00") == 12
assert hex_key("") == 0
