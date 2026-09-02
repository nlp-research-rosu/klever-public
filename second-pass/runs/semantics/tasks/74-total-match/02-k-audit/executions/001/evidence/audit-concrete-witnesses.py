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
assert total_match([""], []) == [""]
assert total_match(["a"], ["b"]) == ["a"]
assert total_match(["a"], ["bb"]) == ["a"]
assert total_match(["ab"], ["x"]) == ["x"]
assert total_match(["ab", "c"], ["x", "yz"]) == ["ab", "c"]
assert total_match(["", ""], [""]) == ["", ""]
