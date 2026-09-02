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


case_empty = correct_bracketing("")
case_open = correct_bracketing("(")
case_close = correct_bracketing(")")
case_pair = correct_bracketing("()")
case_nested = correct_bracketing("(()())")
case_bad_prefix = correct_bracketing(")(()")
case_concat = correct_bracketing("()()")
