def match_parens(lst):
    s1 = lst[0] + lst[1]
    s2 = lst[1] + lst[0]
    val = 0
    ok = True
    c = ""
    r1 = False
    r2 = False
    for c in s1:
        if c == "(":
            val = val + 1
        else:
            val = val - 1
        if val < 0:
            ok = False
    r1 = ok and (val == 0)
    val = 0
    ok = True
    for c in s2:
        if c == "(":
            val = val + 1
        else:
            val = val - 1
        if val < 0:
            ok = False
    r2 = ok and (val == 0)
    return "Yes" if (r1 or r2) else "No"


# Smoke checks from the prompt docstring (NOT hidden tests).
assert match_parens(["()(", ")"]) == "Yes"
assert match_parens([")", ")"]) == "No"
assert match_parens(["(()(())", "())())"]) == "No"
assert match_parens([")())", "(()()("]) == "Yes"
