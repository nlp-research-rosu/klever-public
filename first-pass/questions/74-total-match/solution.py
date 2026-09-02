def total_match(lst1, lst2):
    l1 = 0
    s = ""
    for s in lst1:
        l1 = l1 + len(s)
    l2 = 0
    for s in lst2:
        l2 = l2 + len(s)
    result = lst2
    if l1 <= l2:
        result = lst1
    return result
