def next_smallest(lst):
    distinct = sorted(set(lst))
    return distinct[1] if len(distinct) > 1 else None
