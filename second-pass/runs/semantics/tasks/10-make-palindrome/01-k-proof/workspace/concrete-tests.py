def is_palindrome(string: str) -> bool:
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    i = 0
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            return string + string[:i][::-1]
    return string


assert make_palindrome("") == ""
assert make_palindrome("cat") == "catac"
assert make_palindrome("cata") == "catac"
assert make_palindrome("race") == "racecar"
assert make_palindrome("aaaa") == "aaaa"
assert make_palindrome("abac") == "abacaba"
