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


assert change_base(8, 3) == "22"
assert change_base(8, 2) == "1000"
assert change_base(7, 2) == "111"
assert change_base(0, 2) == "0"
assert change_base(-8, 3) == "-22"
assert change_base(-7, 2) == "-111"
assert change_base(12345, 9) == "17836"
