def is_nested(string):
    state = 0
    char = ''
    for char in string:
        if ord(char) == 91:
            if state < 2:
                state += 1
        else:
            if state > 1:
                if state < 4:
                    state += 1
    return state == 4
