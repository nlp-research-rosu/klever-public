def string_xor(a, b):
    result = ""
    x = ""
    y = ""
    for x, y in zip(a, b):
        if x == y:
            result = result + "0"
        else:
            result = result + "1"
    return result
