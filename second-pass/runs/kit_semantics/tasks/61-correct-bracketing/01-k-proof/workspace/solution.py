def correct_bracketing(brackets: str):
    balance = 0
    valid = True
    for bracket in brackets:
        if bracket == "(":
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            valid = False
    return valid and balance == 0
