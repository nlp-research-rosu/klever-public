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


assert total_match([], []) == []
assert total_match(["hi", "admin"], ["hI", "Hi"]) == ["hI", "Hi"]
assert total_match(
    ["hi", "admin"], ["hi", "hi", "admin", "project"]
) == ["hi", "admin"]
assert total_match(["hi", "admin"], ["hI", "hi", "hi"]) == ["hI", "hi", "hi"]
assert total_match(["4"], ["1", "2", "3", "4", "5"]) == ["4"]
