def how_many_times(string: str, substring: str) -> int:
    if substring == "":
        return len(string) + 1
    if string == "":
        return 0
    return (1 if string.startswith(substring) else 0) + how_many_times(
        string[1:], substring
    )
