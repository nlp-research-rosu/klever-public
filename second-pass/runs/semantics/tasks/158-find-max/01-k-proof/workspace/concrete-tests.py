def find_max(words):
    best = ""
    max_unique = 0
    word = ""
    unique = 0
    for word in words:
        unique = len(set(word))
        if unique > max_unique:
            best = word
            max_unique = unique
        elif unique == max_unique:
            if word < best:
                best = word
    return best


assert find_max(["name", "of", "string"]) == "string"
assert find_max(["name", "enam", "game"]) == "enam"
assert find_max(["aaaaaaa", "bb", "cc"]) == "aaaaaaa"
assert find_max([]) == ""
assert find_max(["xy", "yx", "z"]) == "xy"
