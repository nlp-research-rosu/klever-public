def fix_spaces(text):
    result = ""
    rl = 0
    ch = ""
    for ch in text + chr(0):
        if ch == " ":
            rl = rl + 1
        elif ch == chr(0):
            if rl > 2:
                result = result + "-"
            elif rl > 0:
                result = result + "_"
            rl = 0
        else:
            if rl > 2:
                result = result + "-"
            elif rl == 2:
                result = result + "__"
            elif rl == 1:
                result = result + "_"
            result = result + ch
            rl = 0
    return result
