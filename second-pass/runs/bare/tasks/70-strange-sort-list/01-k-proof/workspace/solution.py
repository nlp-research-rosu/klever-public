def strange_sorted(ordered):
    if len(ordered) == 0:
        return []
    if len(ordered) == 1:
        return ordered
    return [ordered[0], ordered[-1]] + strange_sorted(ordered[1:-1])


def strange_sort_list(lst):
    return strange_sorted(sorted(lst))
