def hex_key(num):
    count = 0
    digit = ""
    for digit in num:
        count += digit in "2357BD"
    return count
