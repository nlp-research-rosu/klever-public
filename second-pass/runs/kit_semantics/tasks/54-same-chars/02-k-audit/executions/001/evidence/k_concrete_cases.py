def same_chars(s0: str, s1: str):
    return set(s0) == set(s1)


case_empty = same_chars("", "")
case_empty_left = same_chars("", "a")
case_duplicate = same_chars("a", "aa")
case_reordered = same_chars("ab", "bbaa")
case_different_left = same_chars("abc", "ab")
case_different_right = same_chars("ab", "abc")
