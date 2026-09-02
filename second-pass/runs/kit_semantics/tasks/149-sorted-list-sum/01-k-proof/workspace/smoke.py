def sorted_list_sum(lst):
    result = []
    word = ""
    for word in lst:
        if len(word) % 2 == 0:
            result.append(word)
    return sorted(sorted(result), key=len)


assert sorted_list_sum([]) == []
assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]
assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]
assert sorted_list_sum(
    ["zz", "b", "aa", "cccc", "bb", "ddd", "aa"]
) == ["aa", "aa", "bb", "zz", "cccc"]
assert sorted_list_sum(["x", "yyy"]) == []
