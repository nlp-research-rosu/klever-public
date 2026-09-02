def move_one_ball(arr):
    if len(arr) == 0:
        return True

    drops = 0
    first = arr[0]
    previous = first

    for current in arr:
        if current < previous:
            drops += 1
        previous = current

    if first < previous:
        drops += 1

    return drops < 2
