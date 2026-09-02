def string_xor(a: str, b: str) -> str:
    if a == "":
        return ""
    if b == "":
        return ""
    if a[0] == b[0]:
        return "0" + string_xor(a[1:], b[1:])
    return "1" + string_xor(a[1:], b[1:])
