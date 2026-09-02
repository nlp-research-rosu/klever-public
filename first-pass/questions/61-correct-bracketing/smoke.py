def correct_bracketing(brackets):
    depth = 0
    for b in brackets:
        if b == "(":
            depth += 1
        else:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


# HumanEval/61 test cases (the dataset `check`); correct_bracketing returns a bool.
assert correct_bracketing("()")
assert correct_bracketing("(()())")
assert correct_bracketing("()()(()())()")
assert correct_bracketing("()()((()()())())(()()(()))")
assert not correct_bracketing("((()())))")
assert not correct_bracketing(")(()")
assert not correct_bracketing("(")
assert not correct_bracketing("((((")
assert not correct_bracketing(")")
assert not correct_bracketing("(()")
assert not correct_bracketing("()()(()())())(()")
assert not correct_bracketing("()()(()())()))()")
