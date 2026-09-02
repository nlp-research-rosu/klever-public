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


cases = [
    ([-3, -4], [False]),
    ([-3, True], [2]),
    ([-3.0, -4.0], [0.0]),
    ([-3.5, -2.5], [4.0]),
    ([True, False, -2.0], [-3, 6]),
]

for left, right in cases:
    print(left, right, exchange(left, right))

for value in [-4, -3, False, True, -4.0, -3.0, -3.5]:
    print("parity", repr(value), value % 2, value % 2 == 0)
