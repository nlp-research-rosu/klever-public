def digitSum(s):
    total = 0
    char = ""
    for char in s:
        if char.isupper():
            total += ord(char)
    return total


assert digitSum("") == 0
assert digitSum("abAB") == 131
assert digitSum("abcCd") == 67
assert digitSum("helloE") == 69
assert digitSum("woArBld") == 131
assert digitSum("aAaaaXa") == 153
