def file_name_check(file_name):
    """Return "Yes" exactly when file_name satisfies the prompt's rules."""
    if file_name.count(".") != 1:
        return "No"

    # A valid name has at least one character, one dot, and a 3-letter suffix.
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
