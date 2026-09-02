def hex_key(num):
    count = 0
    digit = ""
    for digit in num:
        count += digit in "2357BD"
    return count


assert hex_key("") == 0
assert hex_key("AB") == 1
assert hex_key("1077E") == 2
assert hex_key("ABED1A33") == 4
assert hex_key("123456789ABCDEF0") == 6
assert hex_key("2020") == 2
assert hex_key("2357BD") == 6
assert hex_key("014689ACEF") == 0
assert hex_key("22222222") == 8
assert hex_key("FFFFFFFF") == 0
assert hex_key("BD2") == 3
