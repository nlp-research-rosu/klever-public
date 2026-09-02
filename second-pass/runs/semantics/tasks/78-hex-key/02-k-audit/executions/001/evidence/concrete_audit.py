def hex_key(num):
    count = 0
    digit = ""
    for digit in num:
        if digit in "2357BD":
            count += 1
    return count


# Prompt examples, empty input, every one-character branch, and mixed boundaries.
assert hex_key("") == 0
assert hex_key("AB") == 1
assert hex_key("1077E") == 2
assert hex_key("ABED1A33") == 4
assert hex_key("123456789ABCDEF0") == 6
assert hex_key("2020") == 2
assert hex_key("0") == 0
assert hex_key("1") == 0
assert hex_key("2") == 1
assert hex_key("3") == 1
assert hex_key("4") == 0
assert hex_key("5") == 1
assert hex_key("6") == 0
assert hex_key("7") == 1
assert hex_key("8") == 0
assert hex_key("9") == 0
assert hex_key("A") == 0
assert hex_key("B") == 1
assert hex_key("C") == 0
assert hex_key("D") == 1
assert hex_key("E") == 0
assert hex_key("F") == 0
assert hex_key("2357BD") == 6
assert hex_key("014689ACEF") == 0
