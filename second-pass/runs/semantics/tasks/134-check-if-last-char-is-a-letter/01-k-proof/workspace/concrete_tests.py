def check_if_last_char_is_a_letter(txt):
    if len(txt) == 0:
        return False
    if not txt[-1].isalpha():
        return False
    if len(txt) == 1:
        return True
    return txt[-2] == " "


assert check_if_last_char_is_a_letter("apple pie") == False
assert check_if_last_char_is_a_letter("apple pi e") == True
assert check_if_last_char_is_a_letter("apple pi e ") == False
assert check_if_last_char_is_a_letter("") == False
assert check_if_last_char_is_a_letter("a") == True
assert check_if_last_char_is_a_letter("7") == False
assert check_if_last_char_is_a_letter("ab") == False
assert check_if_last_char_is_a_letter("a b") == True
assert check_if_last_char_is_a_letter("a !") == False
