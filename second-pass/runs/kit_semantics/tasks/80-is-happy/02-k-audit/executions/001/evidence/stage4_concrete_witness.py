def is_happy(s):
    happy = True
    previous2 = -1
    previous1 = -1
    i = 0
    ch = ""
    code = 0
    for ch in s:
        code = ord(ch)
        if i >= 2 and (code == previous1 or code == previous2 or previous1 == previous2):
            happy = False
        previous2 = previous1
        previous1 = code
        i = i + 1

    return i >= 3 and happy


assert is_happy("") == False
assert is_happy("a") == False
assert is_happy("aa") == False
assert is_happy("abc") == True
assert is_happy("aba") == False
assert is_happy("abca") == True
assert is_happy("abac") == False
