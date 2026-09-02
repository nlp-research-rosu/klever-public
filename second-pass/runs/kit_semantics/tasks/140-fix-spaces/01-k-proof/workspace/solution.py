def fix_spaces(text):
    result = ""
    spaces = ""
    char = ""
    for char in text:
        if char == " ":
            if spaces == "__":
                spaces = "-"
            elif spaces != "-":
                spaces += "_"
        else:
            result += spaces + char
            spaces = ""
    return result + spaces
