def sort_even(l):
    n = len(l)
    evens = []
    se = []
    ans = []
    k = 0
    i = 0
    for k in range(0, n):
        if k % 2 == 0:
            evens = evens + [l[k]]
    se = sorted(evens)
    for i in range(0, n):
        if i % 2 == 0:
            ans = ans + [se[i // 2]]
        else:
            ans = ans + [l[i]]
    return ans


# Smoke checks from the prompt docstring (NOT hidden tests).
assert sort_even([1, 2, 3]) == [1, 2, 3]
assert sort_even([5, 6, 3, 4]) == [3, 6, 5, 4]
