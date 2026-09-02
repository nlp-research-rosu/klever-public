def move_one_ball(arr):
    drops = 0
    previous = arr[-1]
    for value in arr:
        if previous > value:
            drops = drops + 2
        previous = value
    return drops
