def compare_one(a, b):
    a_value = a
    b_value = b

    if isinstance(a, str):
        a_value = float(a.replace(",", "."))
    if isinstance(b, str):
        b_value = float(b.replace(",", "."))

    if a_value == b_value:
        return None
    if a_value > b_value:
        return a
    return b


assert compare_one(1, 2) == 2
assert compare_one(1, 2.5) == 2.5
assert compare_one(1, "2,3") == "2,3"
assert compare_one(2.5, 1) == 2.5
assert compare_one(1.0, 1.0) is None
assert compare_one(3.0, "3,0") is None
assert compare_one("1", 1) is None
assert compare_one("2,5", 2.0) == "2,5"
assert compare_one("5,1", "6") == "6"
