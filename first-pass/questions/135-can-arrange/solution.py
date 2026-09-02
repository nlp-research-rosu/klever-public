def can_arrange(arr):
    ind = -1
    i = 0
    prev = 0
    x = 0
    for x in arr:
        if i >= 1:
            if x < prev:
                ind = i
        prev = x
        i = i + 1
    return ind
