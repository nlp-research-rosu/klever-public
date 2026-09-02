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
