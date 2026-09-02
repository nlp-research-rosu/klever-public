def is_bored(S):
    count = 0
    state = 0
    ch = ""
    code = 0
    for ch in S:
        code = ord(ch)
        if code == 46 or code == 63 or code == 33:
            state = 0
        elif state == 0:
            if code == 32 or (code >= 9 and code <= 13):
                state = 0
            elif code == 73:
                state = 1
            else:
                state = 2
        elif state == 1:
            if code == 32:
                count += 1
            state = 2
    return count
