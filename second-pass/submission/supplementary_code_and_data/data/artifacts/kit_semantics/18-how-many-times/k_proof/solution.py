def how_many_times(string: str, substring: str) -> int:
    if substring == "":
        return len(string) + 1

    count = 0
    while string != "":
        if string.startswith(substring):
            count += 1
        string = string[1:]

    return count
