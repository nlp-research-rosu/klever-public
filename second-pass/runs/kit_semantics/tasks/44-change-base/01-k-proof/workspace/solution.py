def change_base(x: int, base: int):
    if x == 0:
        return "0"
    sign = ""
    if x < 0:
        sign = "-"
        x = -x
    result = ""
    while x > 0:
        result = chr(48 + x % base) + result
        x = x // base
    return sign + result
