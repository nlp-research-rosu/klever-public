def separate_paren_groups(paren_string):
    result = []
    current = ""
    depth = 0
    c = ""
    for c in paren_string:
        if c == "(":
            current = current + c
            depth = depth + 1
        elif c == ")":
            current = current + c
            depth = depth - 1
            if depth == 0:
                result = result + [current]
                current = ""
    return result


# HumanEval/1 test cases (the dataset `check`); returns a list of strings.
assert separate_paren_groups("(()()) ((())) () ((())()())") == ["(()())", "((()))", "()", "((())()())"]
assert separate_paren_groups("() (()) ((())) (((())))") == ["()", "(())", "((()))", "(((())))"]
assert separate_paren_groups("(()(())((())))") == ["(()(())((())))"]
assert separate_paren_groups("( ) (( )) (( )( ))") == ["()", "(())", "(()())"]
