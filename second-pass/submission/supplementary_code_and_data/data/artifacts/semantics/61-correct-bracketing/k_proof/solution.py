def correct_bracketing(brackets: str):
    balance = 0
    bracket = ""
    for bracket in brackets:
        if bracket == "(":
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0
