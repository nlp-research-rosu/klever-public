def move_one_ball(arr):
    drops = 0
    previous = arr[-1]
    for value in arr:
        if previous > value:
            drops = drops + 1
        previous = value
    return previous + drops

