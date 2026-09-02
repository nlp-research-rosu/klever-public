def incr_list(l: list):
    result = []
    x = 0
    for x in l:
        result.append(x + 1)
    return result


assert incr_list([]) == []
assert incr_list([1, 2, 3]) == [2, 3, 4]
assert incr_list([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [6, 4, 6, 3, 4, 4, 10, 1, 124]
assert incr_list([True, False, 2.5, -1]) == [2, 1, 3.5, 0]
