# sorted(list) — trusted ascending sort primitive (opaque symbolic for kprove, concrete
# insertion sort for krun). Int lists only.
assert sorted([3, 1, 2, 1]) == [1, 1, 2, 3]
assert sorted([]) == []
assert sorted([5]) == [5]
assert sorted([-2, 4, -1, 0, 4]) == [-2, -1, 0, 4, 4]
assert sorted([10, 9, 8, 7, 6]) == [6, 7, 8, 9, 10]
