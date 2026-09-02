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


assert exchange([1.0, 2.0], [4.0]) == "YES"
assert exchange([1.5, 2.0], [3.5]) == "NO"
assert exchange([-4.0, -3.0], [0.0]) == "YES"
assert exchange([-1.5], [2.0]) == "YES"
assert exchange([2.5, -3.5], [4.25]) == "NO"
assert exchange([True, False], [2]) == "YES"
assert exchange([True], [False]) == "YES"
assert exchange([True, True], [False]) == "NO"
assert exchange([1, 3.0], [2.0, False]) == "YES"
assert exchange([2.0, True, 4], [3.5]) == "NO"
assert exchange([2.0, False, 4], [3.5]) == "YES"
