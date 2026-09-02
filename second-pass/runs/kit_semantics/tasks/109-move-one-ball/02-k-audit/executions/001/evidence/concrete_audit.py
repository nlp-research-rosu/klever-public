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


assert move_one_ball([]) == True
assert move_one_ball([7]) == True
assert move_one_ball([3, 4, 5, 1, 2]) == True
assert move_one_ball([3, 5, 4, 1, 2]) == False
assert move_one_ball([-1, 5]) == True
assert move_one_ball([5, -1]) == True
assert move_one_ball([2, 1, 3]) == False
