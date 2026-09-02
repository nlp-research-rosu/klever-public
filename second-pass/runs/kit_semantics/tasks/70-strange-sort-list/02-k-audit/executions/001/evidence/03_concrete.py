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


case_empty = strange_sort_list([])
case_singleton = strange_sort_list([9])
case_even = strange_sort_list([1, 2, 3, 4])
case_duplicates = strange_sort_list([5, 5, 5, 5])
case_odd_negative = strange_sort_list([4, -1, 3, 2, 0])
