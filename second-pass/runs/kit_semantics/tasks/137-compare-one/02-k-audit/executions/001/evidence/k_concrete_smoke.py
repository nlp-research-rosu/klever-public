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


# Docstring examples, all comparison outcomes, and representative type pairs.
assert compare_one(1, 2.5) == 2.5
assert compare_one(1, "2,3") == "2,3"
assert compare_one("5,1", "6") == "6"
assert compare_one("1", 1) is None
assert compare_one(-1, -2) == -1
assert compare_one(-2.5, -1) == -1
assert compare_one("2.50", "2,5") is None
assert compare_one(2.5, "2") == 2.5
