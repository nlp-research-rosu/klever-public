def pairs_sum_to_zero(l):
    if not l:
        return False
    if -l[0] in l[1:]:
        return True
    return pairs_sum_to_zero(l[1:])
