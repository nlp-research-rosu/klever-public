def digitSum(s):
    result = 0
    c = ""
    for c in s:
        code = ord(c)
        if code >= 65:
            if code <= 90:
                result = result + code
    return result
