def how_many_times(string: str, substring: str) -> int:
    if substring == "":
        return len(string) + 1

    count = 0
    while string != "":
        if string.startswith(substring):
            count += 1
        string = string[1:]

    return count


case_empty_nonempty = how_many_times("", "a")
case_empty_empty = how_many_times("", "")
case_single = how_many_times("a", "a")
case_pattern_longer = how_many_times("a", "aa")
case_prompt_single = how_many_times("aaa", "a")
case_prompt_overlap = how_many_times("aaaa", "aa")
case_overlap_three = how_many_times("aaaaa", "aaa")
case_shifted_overlap = how_many_times("ababa", "aba")
case_no_match = how_many_times("abc", "z")
case_empty_pattern = how_many_times("abc", "")
