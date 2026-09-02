def is_nested(string):
    state = 0
    bracket = ""
    for bracket in string:
        if state < 2:
            if bracket == "[":
                state += 1
        elif state < 4:
            if bracket == "]":
                state += 1
    return state == 4
