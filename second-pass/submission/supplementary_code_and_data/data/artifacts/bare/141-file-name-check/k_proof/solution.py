def file_name_check(file_name):
    digits = (
        file_name.count("0")
        + file_name.count("1")
        + file_name.count("2")
        + file_name.count("3")
        + file_name.count("4")
        + file_name.count("5")
        + file_name.count("6")
        + file_name.count("7")
        + file_name.count("8")
        + file_name.count("9")
    )
    if file_name.count(".") != 1:
        return "No"
    if digits > 3:
        return "No"
    if len(file_name) == 0:
        return "No"
    first = file_name[0]
    if not (("a" <= first and first <= "z") or ("A" <= first and first <= "Z")):
        return "No"
    if (
        file_name.endswith(".txt")
        or file_name.endswith(".exe")
        or file_name.endswith(".dll")
    ):
        return "Yes"
    return "No"
