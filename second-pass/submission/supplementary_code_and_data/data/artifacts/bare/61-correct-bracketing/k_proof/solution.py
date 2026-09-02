def correct_bracketing(brackets: str):
    count = 0
    for bracket in brackets:
        if bracket == "(":
            count = count + 1
        else:
            if count == 0:
                return False
            count = count - 1
    return count == 0
