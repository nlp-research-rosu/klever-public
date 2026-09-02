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
