def pairs_sum_to_zero(l):
    n = len(l)
    found = False
    i = 0
    j = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            if l[i] + l[j] == 0:
                found = True
    return found


# Smoke checks from the prompt docstring (NOT hidden tests).
assert not pairs_sum_to_zero([1, 3, 5, 0])
assert not pairs_sum_to_zero([1, 3, -2, 1])
assert not pairs_sum_to_zero([1, 2, 3, 7])
assert pairs_sum_to_zero([2, 4, -5, 3, 5, 7])
assert not pairs_sum_to_zero([1])
