def check_if_last_char_is_a_letter(txt):
    last = 0
    prev = 0
    n = 0
    ch = ""
    for ch in txt:
        prev = last
        last = ord(ch)
        n = n + 1
    isletter = (97 <= last and last <= 122) or (65 <= last and last <= 90)
    isolated = (n == 1) or (prev == 32)
    return isletter and isolated


# Smoke checks from the prompt docstring (NOT hidden tests).
assert check_if_last_char_is_a_letter("apple pie") == False
assert check_if_last_char_is_a_letter("apple pi e") == True
assert check_if_last_char_is_a_letter("apple pi e ") == False
assert check_if_last_char_is_a_letter("") == False
assert check_if_last_char_is_a_letter("A") == True
