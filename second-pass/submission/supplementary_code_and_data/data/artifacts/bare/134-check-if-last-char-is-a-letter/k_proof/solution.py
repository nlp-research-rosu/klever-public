def check_if_last_char_is_a_letter(txt):
    return ((len(txt) == 1 and txt.isalpha())
            or (len(txt) > 1 and txt[-1].isalpha() and txt[-2] == " "))
