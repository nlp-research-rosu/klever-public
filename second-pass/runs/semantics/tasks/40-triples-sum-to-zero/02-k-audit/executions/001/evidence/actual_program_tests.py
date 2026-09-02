def triples_sum_to_zero(l: list):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            for k in range(j + 1, len(l)):
                if l[i] + l[j] + l[k] == 0:
                    return True
    return False


assert triples_sum_to_zero([]) == False
assert triples_sum_to_zero([0]) == False
assert triples_sum_to_zero([0, 0]) == False
assert triples_sum_to_zero([0, 0, 0]) == True
assert triples_sum_to_zero([-1, 0, 2]) == False
assert triples_sum_to_zero([50, 60, -3, 1, 2]) == True
assert triples_sum_to_zero([9, 8, 7, 6, -5, 2, 3]) == True
assert triples_sum_to_zero([9, 8, 7, 6, 5, 4, 3]) == False
