#!/usr/bin/env python3
"""Reviewer-authored concrete K probe using the submitted function body."""


def correct_bracketing(brackets: str):
    balance = 0
    valid = True
    bracket = ""
    for bracket in brackets:
        if bracket == "<":
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            valid = False
    return valid and balance == 0


# Documented examples.
assert correct_bracketing("<") == False
assert correct_bracketing("<>") == True
assert correct_bracketing("<<><>>") == True
assert correct_bracketing("><<>") == False

# Empty, both branch directions, prefix failure, nesting, and concatenation.
assert correct_bracketing("") == True
assert correct_bracketing(">") == False
assert correct_bracketing("<<") == False
assert correct_bracketing("<<>>") == True
assert correct_bracketing("<><>") == True
assert correct_bracketing("<>>") == False
assert correct_bracketing("<<<>>>") == True
assert correct_bracketing(">>><<<") == False
