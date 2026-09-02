def file_name_check(file_name):
    if file_name.count(".") != 1:
        return "No"
    if file_name[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return "No"
    if not (
        file_name[-4:] == ".txt"
        or file_name[-4:] == ".exe"
        or file_name[-4:] == ".dll"
    ):
        return "No"
    if (
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
        > 3
    ):
        return "No"
    return "Yes"


assert file_name_check("") == "No"
assert file_name_check(".txt") == "No"
assert file_name_check("a") == "No"
assert file_name_check("a.b.txt") == "No"
assert file_name_check("1.txt") == "No"
assert file_name_check("_a.txt") == "No"
assert file_name_check("a.pdf") == "No"
assert file_name_check("a.txt") == "Yes"
assert file_name_check("a.exe") == "Yes"
assert file_name_check("a.dll") == "Yes"
assert file_name_check("A0b1c2.txt") == "Yes"
assert file_name_check("A0b1c23.txt") == "No"
assert file_name_check("example.txt") == "Yes"
assert file_name_check("1example.dll") == "No"
