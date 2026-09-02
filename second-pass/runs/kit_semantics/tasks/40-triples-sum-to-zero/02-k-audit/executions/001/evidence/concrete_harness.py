def triples_sum_to_zero(l: list):
    found = False
    i = 0
    j = 0
    k = 0
    while i < len(l):
        j = i + 1
        while j < len(l):
            k = j + 1
            while k < len(l):
                if l[i] + l[j] + l[k] == 0:
                    found = True
                k += 1
            k = 0
            j += 1
        j = 0
        i += 1
    return found


# Prompt examples and loop/branch boundaries.
assert not triples_sum_to_zero([1, 3, 5, 0])
assert triples_sum_to_zero([1, 3, -2, 1])
assert not triples_sum_to_zero([1, 2, 3, 7])
assert triples_sum_to_zero([2, 4, -5, 3, 9, 7])
assert not triples_sum_to_zero([1])
assert not triples_sum_to_zero([])
assert not triples_sum_to_zero([0])
assert not triples_sum_to_zero([0, 0])
assert triples_sum_to_zero([0, 0, 0])
assert triples_sum_to_zero(
    [1000000000000000000000000000000, -1000000000000000000000000000000, 0]
)
