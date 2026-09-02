def total_match(lst1, lst2):
    total1 = 0
    total2 = 0

    for item in lst1:
        total1 += len(item)

    for item in lst2:
        total2 += len(item)

    if total1 <= total2:
        return lst1
    return lst2


assert total_match([], []) == []
assert total_match(["hi", "admin"], ["hI", "Hi"]) == ["hI", "Hi"]
assert total_match(
    ["hi", "admin"], ["hi", "hi", "admin", "project"]
) == ["hi", "admin"]
assert total_match(["hi", "admin"], ["hI", "hi", "hi"]) == ["hI", "hi", "hi"]
assert total_match(["4"], ["1", "2", "3", "4", "5"]) == ["4"]
