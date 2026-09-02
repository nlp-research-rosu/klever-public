def compare_one(a, b):
    if isinstance(a, str):
        a_value = float(a.replace(",", "."))
    else:
        a_value = a

    if isinstance(b, str):
        b_value = float(b.replace(",", "."))
    else:
        b_value = b

    if a_value > b_value:
        return a
    if b_value > a_value:
        return b
    return None


assert compare_one(1, 2.5) == 2.5
assert compare_one(1, "2,3") == "2,3"
assert compare_one("5,1", "6") == "6"
assert compare_one("1", 1) is None
assert compare_one(-2, "-2.5") == -2
assert compare_one(2, 1) == 2
assert compare_one(2.5, 1) == 2.5
assert compare_one(2, 2.5) == 2.5
assert compare_one(2.5, 3.5) == 3.5
assert compare_one("2.5", 2) == "2.5"
assert compare_one(2, "2.5") == "2.5"
assert compare_one("2,5", 2.0) == "2,5"
assert compare_one(2.5, "2,0") == 2.5
assert compare_one("2,5", "2.4") == "2,5"
assert compare_one("1.0", "1,00") is None
assert compare_one(-3.5, "-3,5") is None
