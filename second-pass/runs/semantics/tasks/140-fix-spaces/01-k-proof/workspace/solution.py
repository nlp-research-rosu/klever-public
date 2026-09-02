def fix_spaces(text):
    result = ""
    spaces = 0
    char = ""

    for char in text:
        if ord(char) - 32:
            if spaces > 2:
                result += "-"
            elif spaces == 1:
                result += "_"
            elif spaces == 2:
                result += "__"

            result += char
            spaces = 0
        else:
            spaces += 1

    if spaces > 2:
        result += "-"
    elif spaces == 1:
        result += "_"
    elif spaces == 2:
        result += "__"

    return result
