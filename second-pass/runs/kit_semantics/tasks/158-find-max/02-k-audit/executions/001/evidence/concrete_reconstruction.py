def find_max(words):
    result = ""
    max_unique = -1
    word = ""
    unique = -1
    for word in words:
        unique = len(set(word))
        if unique > max_unique or unique == max_unique and word < result:
            result = word
            max_unique = unique
    return result


assert find_max(["name", "of", "string"]) == "string"
assert find_max(["name", "enam", "game"]) == "enam"
assert find_max(["aaaaaaa", "bb", "cc"]) == "aaaaaaa"
assert find_max(["z", "ab"]) == "ab"
assert find_max(["ab", "z"]) == "ab"
assert find_max(["ba", "ab"]) == "ab"
assert find_max(["ab", "ba"]) == "ab"
assert find_max([""]) == ""
assert find_max([]) == ""
