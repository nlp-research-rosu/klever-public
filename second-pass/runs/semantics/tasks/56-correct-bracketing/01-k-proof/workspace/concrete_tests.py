def correct_bracketing(brackets: str):
    """Return whether the angle brackets are correctly balanced."""
    depth = 0
    bracket = ""
    for bracket in brackets:
        if bracket == "<":
            depth += 1
        else:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


assert correct_bracketing("<") == False
assert correct_bracketing("<>") == True
assert correct_bracketing("<<><>>") == True
assert correct_bracketing("><<>") == False
assert correct_bracketing("") == True
assert correct_bracketing("<<>>") == True
assert correct_bracketing("<><>") == True
assert correct_bracketing("<<>") == False
