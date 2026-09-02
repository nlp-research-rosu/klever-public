def how_many_times(string: str, substring: str) -> int:
    if substring == "":
        return len(string) + 1
    if len(string) < len(substring):
        return 0
    if string[:len(substring)] == substring:
        return 1 + how_many_times(string[1:], substring)
    return how_many_times(string[1:], substring)
