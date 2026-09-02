def exchange(lst1, lst2):
    even = 0
    for value in lst1:
        if value % 2 == 0:
            even = even + 1
    for value in lst2:
        if value % 2 == 0:
            even = even + 1
    if even >= len(lst1):
        return "YES"
    return "NO"
