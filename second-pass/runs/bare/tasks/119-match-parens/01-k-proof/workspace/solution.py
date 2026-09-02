def is_balanced(s, depth):
    if depth < 0:
        return False
    if s == "":
        return depth == 0
    if s[0] == "(":
        return is_balanced(s[1:], depth + 1)
    return is_balanced(s[1:], depth - 1)


def match_parens(lst):
    if is_balanced(lst[0] + lst[1], 0):
        return "Yes"
    if is_balanced(lst[1] + lst[0], 0):
        return "Yes"
    return "No"
