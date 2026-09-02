def check_if_last_char_is_a_letter(txt):
    if len(txt) == 0:
        return False
    return txt[-1].isalpha() and (len(txt) == 1 or txt[-2] == " ")


assert check_if_last_char_is_a_letter("apple pie") == False
assert check_if_last_char_is_a_letter("apple pi e") == True
assert check_if_last_char_is_a_letter("apple pi e ") == False
assert check_if_last_char_is_a_letter("") == False
assert check_if_last_char_is_a_letter("A") == True
assert check_if_last_char_is_a_letter("1") == False
assert check_if_last_char_is_a_letter("x Y") == True
assert check_if_last_char_is_a_letter("xy") == False
assert check_if_last_char_is_a_letter("  z") == True
