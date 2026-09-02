def is_palindrome(text):
    for i in range(len(text)):
        if text[i] != text[len(text) - 1 - i]:
            return False
    return True


# HumanEval/48 test cases (the dataset `check`); is_palindrome returns a bool.
assert is_palindrome("")
assert is_palindrome("aba")
assert is_palindrome("aaaaa")
assert not is_palindrome("zbcd")
assert is_palindrome("xywyx")
assert not is_palindrome("xywyz")
assert not is_palindrome("xywzx")
