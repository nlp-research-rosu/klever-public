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
