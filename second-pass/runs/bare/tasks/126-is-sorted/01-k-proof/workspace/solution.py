def is_sorted(lst):
    return lst == sorted(lst) and all(lst.count(x) <= 2 for x in lst)
