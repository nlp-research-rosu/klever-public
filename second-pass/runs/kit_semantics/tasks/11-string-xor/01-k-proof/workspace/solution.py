def string_xor(a: str, b: str) -> str:
    result = ""
    x = ""
    y = ""
    for x, y in zip(a, b):
        if x == y:
            result += "0"
        else:
            result += "1"
    return result
