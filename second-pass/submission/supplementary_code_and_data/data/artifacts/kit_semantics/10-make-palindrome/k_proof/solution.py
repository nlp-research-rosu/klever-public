def is_palindrome(string: str) -> bool:
    """Test if given string is a palindrome."""
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """Return the shortest palindrome that begins with string."""
    reverse_string = ""
    char = ""
    for char in string:
        reverse_string = char + reverse_string

    prefix = ""
    reverse_prefix = ""
    found = string == reverse_string
    result = string if found else string + reverse_string

    for char in string:
        if not found:
            prefix = prefix + char
            reverse_prefix = char + reverse_prefix
            if string + reverse_prefix == prefix + reverse_string:
                result = string + reverse_prefix
                found = True

    return result
