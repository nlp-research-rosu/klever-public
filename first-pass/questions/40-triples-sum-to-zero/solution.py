def triples_sum_to_zero(l):
    n = len(l)
    found = False
    i = 0
    j = 0
    k = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if l[i] + l[j] + l[k] == 0:
                    found = True
    return found
