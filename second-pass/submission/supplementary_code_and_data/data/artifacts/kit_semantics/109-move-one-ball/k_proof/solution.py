def move_one_ball(arr):
    if not arr:
        return True

    first = arr[0]
    previous = first
    current = first
    drops = 0

    for current in arr:
        drops = drops + (current < previous)
        previous = current

    drops = drops + (first < previous)

    return drops <= 1
