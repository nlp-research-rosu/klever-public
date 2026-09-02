def digitSum(s):
    result = 0
    char = ""
    code = 0
    for char in s:
        code = ord(char)
        if code >= 65 and code <= 90:
            result += code
    return result


assert digitSum("") == 0
assert digitSum("abAB") == 131
assert digitSum("@A[Z") == 155
assert digitSum("É") == 0
assert digitSum("Ω") == 0
