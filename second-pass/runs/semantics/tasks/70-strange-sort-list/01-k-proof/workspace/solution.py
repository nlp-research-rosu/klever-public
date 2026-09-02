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
