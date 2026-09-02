def pairs_sum_to_zero(l):
    seen = []
    value = 0
    for value in l:
        if -value in seen:
            return True
        seen.append(value)
    return False


assert pairs_sum_to_zero([]) == False
assert pairs_sum_to_zero([0]) == False
assert pairs_sum_to_zero([0, 0]) == True
assert pairs_sum_to_zero([1, -1]) == True
assert pairs_sum_to_zero([1, 2, -1]) == True
assert pairs_sum_to_zero([1, 2, 3]) == False
assert pairs_sum_to_zero([2, 4, -5, 3, 5, 7]) == True
assert pairs_sum_to_zero([-8, 3, 8]) == True
