def monotonic(l):
    inc = True
    dec = True
    i = 0
    prev = 0
    x = 0
    for x in l:
        if i >= 1:
            if x < prev:
                inc = False
            if x > prev:
                dec = False
        prev = x
        i = i + 1
    return inc or dec
