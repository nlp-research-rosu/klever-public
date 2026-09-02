def compare_one(a, b):
    if type(a) == str:
        a_value = float(a.replace(",", "."))
    else:
        a_value = float(a)
    if type(b) == str:
        b_value = float(b.replace(",", "."))
    else:
        b_value = float(b)
    if a_value == b_value:
        return None
    if a_value > b_value:
        return a
    return b
