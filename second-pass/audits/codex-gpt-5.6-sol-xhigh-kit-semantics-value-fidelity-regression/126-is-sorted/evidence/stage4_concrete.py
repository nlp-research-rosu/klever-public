def is_sorted(lst):
    result = lst == sorted(lst)
    current = 0
    for current in lst:
        if lst.count(current) > 2:
            result = False
    return result


result_empty = is_sorted([])
result_two_duplicates = is_sorted([0, 0])
result_three_duplicates = is_sorted([0, 0, 0])
result_unsorted = is_sorted([1, 0])
result_large = is_sorted([0, 10000000000000000000000000000000000000000])
