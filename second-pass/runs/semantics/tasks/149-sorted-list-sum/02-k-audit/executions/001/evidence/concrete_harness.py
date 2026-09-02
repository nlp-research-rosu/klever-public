def sorted_list_sum(lst):
    even_words = []
    for word in lst:
        if len(word) % 2 == 0:
            even_words.append(word)
    return sorted(sorted(even_words), key=len)


assert sorted_list_sum(["aa", "a", "aaa"]) == ["aa"]
assert sorted_list_sum(["ab", "a", "aaa", "cd"]) == ["ab", "cd"]
assert sorted_list_sum([]) == []
assert sorted_list_sum([""]) == [""]
assert sorted_list_sum(["a"]) == []
assert sorted_list_sum(["aa"]) == ["aa"]
assert sorted_list_sum(["aaa"]) == []
assert sorted_list_sum(["ba", "ab", "aa", "ab"]) == ["aa", "ab", "ab", "ba"]
assert sorted_list_sum(["dddd", "bb", "cccc", "aa", "x"]) == [
    "aa",
    "bb",
    "cccc",
    "dddd",
]
