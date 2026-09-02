"""Concrete MPY probes using an exact copy of the submitted function body."""


def exchange(lst1, lst2):
    odd = 0
    even = 0
    number = 0
    for number in lst1:
        if number % 2 != 0:
            odd += 1
    for number in lst2:
        if number % 2 == 0:
            even += 1
    if odd <= even:
        return "YES"
    return "NO"


assert exchange([1, 2, 3, 4], [1, 2, 3, 4]) == "YES"
assert exchange([1, 2, 3, 4], [1, 5, 3, 4]) == "NO"
assert exchange([2], [1]) == "YES"
assert exchange([1], [2]) == "YES"
assert exchange([1, 3], [2]) == "NO"
assert exchange([-3, -2], [-4, 5]) == "YES"
assert exchange([-5], [-3]) == "NO"
assert exchange([], []) == "YES"
assert exchange([100000000000000000001], [-100000000000000000000]) == "YES"
