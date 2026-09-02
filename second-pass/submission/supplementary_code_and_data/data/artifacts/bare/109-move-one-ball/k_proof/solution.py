def move_one_ball(arr):
    if len(arr) == 0:
        return True
    drops = 0
    previous = arr[-1]
    for value in arr:
        if previous > value:
            drops = drops + 1
        previous = value
    return drops <= 1
