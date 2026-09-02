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


# CPython parses exponent notation as the real number 100.0.
assert compare_one("1e2", 500.0) == 500.0
