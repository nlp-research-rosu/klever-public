def reverse_then_continue(q):
    reversed_copy = q[::-1]
    return sum(reversed_copy) + 7


def sum_then_continue(q):
    total = sum(q)
    return total * 3 - 4


# Distinct reversal outcomes and an observable arithmetic continuation.
assert reverse_then_continue([]) == 7
assert reverse_then_continue([1, 2, 3]) == 13
assert reverse_then_continue([4, -10, 4]) == 5

# Distinct sum outcomes and an observable arithmetic continuation.
assert sum_then_continue([]) == -4
assert sum_then_continue([1, 2, 3]) == 14
assert sum_then_continue([4, -10, 4]) == -10
