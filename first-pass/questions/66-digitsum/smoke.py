def digitSum(s):
    result = 0
    c = ""
    for c in s:
        code = ord(c)
        if code >= 65:
            if code <= 90:
                result = result + code
    return result


# HumanEval/66 test cases (the dataset `check`); returns an int.
assert digitSum("") == 0
assert digitSum("abAB") == 131
assert digitSum("abcCd") == 67
assert digitSum("helloE") == 69
assert digitSum("woArBld") == 131
assert digitSum("aAaaaXa") == 153
assert digitSum(" How are yOu?") == 151
assert digitSum("You arE Very Smart") == 327
