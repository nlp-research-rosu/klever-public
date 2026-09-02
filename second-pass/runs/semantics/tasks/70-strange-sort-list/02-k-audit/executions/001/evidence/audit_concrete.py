def strange_sort_list(lst):
    ordered = sorted(lst)
    result = []
    i = 0
    while i < len(ordered):
        if i % 2 == 0:
            result.append(ordered[i // 2])
        else:
            result.append(ordered[len(ordered) - (i // 2) - 1])
        i += 1
    return result


assert strange_sort_list([]) == []
assert strange_sort_list([0]) == [0]
assert strange_sort_list([2, 1]) == [1, 2]
assert strange_sort_list([2, 1, 3]) == [1, 3, 2]
assert strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
assert strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]
assert strange_sort_list([3, -1, 3, 2, 0]) == [-1, 3, 0, 3, 2]
