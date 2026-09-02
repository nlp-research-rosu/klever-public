def digitSum(s):
    result = 0
    char = ""
    code = 0
    for char in s:
        code = ord(char)
        if code >= 65 and code <= 90:
            result += code
    return result
