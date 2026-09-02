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
assert digitSum("abcCd") == 67
assert digitSum("helloE") == 69
assert digitSum("woArBld") == 131
assert digitSum("aAaaaXa") == 153
assert digitSum("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 2015
assert digitSum("0123!@#$abcdefghijklmnopqrstuvwxyz") == 0
