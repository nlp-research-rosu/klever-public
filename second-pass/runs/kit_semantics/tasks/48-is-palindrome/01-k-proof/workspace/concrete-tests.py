def is_palindrome(text: str):
    return text == text[::-1]


assert is_palindrome("") == True
assert is_palindrome("aba") == True
assert is_palindrome("aaaaa") == True
assert is_palindrome("zbcd") == False
assert is_palindrome("ab") == False
