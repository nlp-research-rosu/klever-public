"""Operational-context probe for the installed loop bridge.

The extra assignment is an observable continuation between the loop and the
return. The bridge's exact continuation guard must reject this configuration,
leaving the supplied rules to execute it normally.
"""


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
    valid = False
    return valid and balance == 0


context_result = correct_bracketing("()")
