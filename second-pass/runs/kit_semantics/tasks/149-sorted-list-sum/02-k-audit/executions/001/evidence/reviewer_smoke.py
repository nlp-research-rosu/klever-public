def sorted_list_sum(lst):
    result = []
    word = ""
    for word in lst:
        if len(word) % 2 == 0:
            result.append(word)
    return sorted(sorted(result), key=len)


# Prompt examples and branch/boundary witnesses.
assert sorted_list_sum([]) == []
assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]
assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]
assert sorted_list_sum(["", "x", "bb", "aa", "ccc", "dddd", "aa"]) == [
    "",
    "aa",
    "aa",
    "bb",
    "dddd",
]
assert sorted_list_sum(["x", "yyy"]) == []
