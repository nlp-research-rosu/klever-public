def strlen(string: str) -> int:
    return len(string)


assert strlen("") == 0
assert strlen("abc") == 3
assert strlen("a b") == 3
assert strlen("0123456789") == 10
