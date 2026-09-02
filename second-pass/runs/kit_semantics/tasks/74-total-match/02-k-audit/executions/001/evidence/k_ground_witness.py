def _total_length(strings):
    total = 0
    string = None
    for string in strings:
        total += len(string)
    return total


def total_match(lst1, lst2):
    if _total_length(lst1) <= _total_length(lst2):
        return lst1
    return lst2


# Satisfies entry-first through equality: totalLen(["a"]) = totalLen(["b"]) = 1.
assert total_match(["a"], ["b"]) == ["a"]

# Satisfies entry-first through strict inequality: 0 < 1.
assert total_match([""], ["a"]) == [""]

# Satisfies entry-second: 1 > 0.
assert total_match(["a"], [""]) == [""]
