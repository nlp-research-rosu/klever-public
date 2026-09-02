def file_name_check(file_name):
    """Return "Yes" exactly when file_name satisfies the prompt's rules."""
    if file_name.count(".") != 1:
        return "No"

    if len(file_name) < 5:
        return "No"

    first_code = ord(file_name[0])
    if not (
        (first_code >= 65 and first_code <= 90)
        or (first_code >= 97 and first_code <= 122)
    ):
        return "No"

    suffix = file_name[-4:]
    if not (suffix == ".txt" or suffix == ".exe" or suffix == ".dll"):
        return "No"

    digit_count = (
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
    if digit_count > 3:
        return "No"

    return "Yes"


assert file_name_check("example.txt") == "Yes"
assert file_name_check("1example.dll") == "No"
assert file_name_check("a.exe") == "Yes"
assert file_name_check("Z9.dll") == "Yes"
assert file_name_check("a123.txt") == "Yes"
assert file_name_check("a1234.txt") == "No"
assert file_name_check(".txt") == "No"
assert file_name_check("a..txt") == "No"
assert file_name_check("a.pdf") == "No"
assert file_name_check("a.txtx") == "No"
assert file_name_check("_a.txt") == "No"
