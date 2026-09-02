def strange_sort_list(lst):
    ordered = sorted(lst)
    result = []
    left = 0
    right = len(ordered) - 1
    while left < right:
        result.append(ordered[left])
        result.append(ordered[right])
        left += 1
        right -= 1
    if left == right:
        result.append(ordered[left])
    return result


assert strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
assert strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]
assert strange_sort_list([]) == []
assert strange_sort_list([3, -1, 3, 2, 0]) == [-1, 3, 0, 3, 2]
