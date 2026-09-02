def digitSum(s):
    total = 0
    if "A" <= s <= "Z":
        total = total + ord(s)
    return total
