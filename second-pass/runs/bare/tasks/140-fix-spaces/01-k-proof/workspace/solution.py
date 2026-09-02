def _drop_spaces(text):
    if text == "":
        return ""
    if text[0] == " ":
        return _drop_spaces(text[1:])
    return fix_spaces(text)


def fix_spaces(text):
    if text == "":
        return ""
    if text[0] == " ":
        if len(text) > 2:
            if text[0:3] == "   ":
                return "-" + _drop_spaces(text[3:])
        return "_" + fix_spaces(text[1:])
    return text[0] + fix_spaces(text[1:])
