def digitSum(s):
    total = 0
    char = ""
    for char in s:
        if char.isupper():
            total += ord(char)
    return total


assert digitSum("") == 0
assert digitSum("@AZ[") == 155
assert digitSum("abAB") == 131
assert digitSum("abcCd") == 67
