def sorted_list_sum(lst):
    even_words = []
    for word in lst:
        if len(word) % 2 == 0:
            even_words.append(word)
    return sorted(sorted(even_words), key=len)


assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]
assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]
assert sorted_list_sum([]) == []
assert sorted_list_sum(["zz", "a", "bbbb", "aa", "cc", "odd"]) == [
    "aa",
    "cc",
    "zz",
    "bbbb",
]
assert sorted_list_sum(["bb", "aa", "bb", "x"]) == ["aa", "bb", "bb"]
