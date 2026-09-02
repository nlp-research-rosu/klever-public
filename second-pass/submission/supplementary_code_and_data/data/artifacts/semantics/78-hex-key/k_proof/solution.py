def hex_key(num):
    count = 0
    digit = ""
    for digit in num:
        if digit in "2357BD":
            count += 1
    return count
