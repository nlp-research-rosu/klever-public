def exchange(lst1, lst2):
    """Return whether exchanges can make every element of lst1 even."""
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
