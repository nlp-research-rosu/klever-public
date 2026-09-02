def pairs_sum_to_zero(l):
    seen = []
    value = 0
    for value in l:
        if -value in seen:
            return True
        seen.append(value)
    return False
