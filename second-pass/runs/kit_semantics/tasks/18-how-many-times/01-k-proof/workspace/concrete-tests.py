def how_many_times(string: str, substring: str) -> int:
    if substring == "":
        return len(string) + 1

    count = 0
    while string != "":
        if string.startswith(substring):
            count += 1
        string = string[1:]

    return count


example_empty = how_many_times("", "a")
example_single = how_many_times("aaa", "a")
example_overlap = how_many_times("aaaa", "aa")
empty_substring = how_many_times("abc", "")
