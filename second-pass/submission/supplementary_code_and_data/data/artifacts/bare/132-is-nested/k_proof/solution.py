def is_nested(string):
    state = 0
    for bracket in string:
        if bracket == "[":
            if state < 2:
                state = state + 1
        else:
            if state == 2:
                state = 3
            else:
                if state == 3:
                    return True
    return False
