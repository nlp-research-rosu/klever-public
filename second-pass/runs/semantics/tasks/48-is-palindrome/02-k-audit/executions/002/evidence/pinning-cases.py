def is_palindrome(text: str):
    return text == text[::-1]


empty_result = is_palindrome("")
odd_result = is_palindrome("aba")
even_result = is_palindrome("abba")
mismatch_result = is_palindrome("zbcd")
