def move_one_ball(arr):
    descents = 0
    i = 0
    prev = 0
    first = 0
    x = 0
    for x in arr:
        if i == 0:
            first = x
        if i >= 1:
            if x < prev:
                descents = descents + 1
        prev = x
        i = i + 1
    if prev > first:
        descents = descents + 1
    return descents <= 1
