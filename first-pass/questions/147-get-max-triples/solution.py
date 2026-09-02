def get_max_triples(n):
    count = 0
    i = 0
    j = 0
    k = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if (((i + 1) * (i + 1) - (i + 1) + 1) + ((j + 1) * (j + 1) - (j + 1) + 1) + ((k + 1) * (k + 1) - (k + 1) + 1)) % 3 == 0:
                    count = count + 1
    return count
