def pairs_sum_to_zero(l):
    found = False
    x = 0
    for x in l:
        if x == 0:
            if l.count(0) > 1:
                found = True
        else:
            if l.count(-x) > 0:
                found = True
    return found


assert pairs_sum_to_zero([1, 3, 5, 0]) == False
assert pairs_sum_to_zero([1, 3, -2, 1]) == False
assert pairs_sum_to_zero([1, 2, 3, 7]) == False
assert pairs_sum_to_zero([2, 4, -5, 3, 5, 7]) == True
assert pairs_sum_to_zero([1]) == False
assert pairs_sum_to_zero([]) == False
assert pairs_sum_to_zero([0]) == False
assert pairs_sum_to_zero([0, 0]) == True
assert pairs_sum_to_zero([-4, 4]) == True
