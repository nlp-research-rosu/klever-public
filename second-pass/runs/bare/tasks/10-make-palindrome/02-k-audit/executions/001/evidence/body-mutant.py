def is_palindrome(string: str) -> bool:
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    # Deliberately false body used only to test whether the proof bridge is
    # sensitive to the program-defined computation that it replaces.
    return "WRONG"
