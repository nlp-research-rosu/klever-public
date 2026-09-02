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


assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == "YES"
assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == "NO"
assert exchange([2], [1]) == "YES"
assert exchange([1], [2]) == "YES"
assert exchange([1], [1]) == "NO"
assert exchange([1, 3, 2], [5, 4]) == "NO"
assert exchange([1, 3, 2], [4, 6]) == "YES"
assert exchange([-4, -3], [-2]) == "YES"
