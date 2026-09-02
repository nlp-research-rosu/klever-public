def is_palindrome(text: str):
    return text == text[::-1]


assert is_palindrome("")
assert is_palindrome("a")
assert is_palindrome("aba")
assert is_palindrome("aaaaa")
assert is_palindrome("abba")
assert not is_palindrome("ab")
assert not is_palindrome("zbcd")
assert not is_palindrome("abca")
assert is_palindrome("éaé")
assert not is_palindrome("éaè")
