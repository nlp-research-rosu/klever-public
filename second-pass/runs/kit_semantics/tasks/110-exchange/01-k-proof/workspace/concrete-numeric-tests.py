def exchange(lst1, lst2):
    even_count = 0
    value = 0
    for value in lst1:
        if value % 2 == 0:
            even_count += 1
    for value in lst2:
        if value % 2 == 0:
            even_count += 1
    if even_count >= len(lst1):
        return "YES"
    return "NO"


assert exchange([1.0, 2.0], [4.0]) == "YES"
assert exchange([True, False], [2]) == "YES"
