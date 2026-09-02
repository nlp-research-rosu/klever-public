def is_palindrome(text: str):
    return text == text[::-1]


assert is_palindrome("")
assert is_palindrome("aba")
assert is_palindrome("aaaaa")
assert not is_palindrome("zbcd")
assert is_palindrome("abccba")
assert not is_palindrome("abca")
