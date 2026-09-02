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


assert move_one_ball([]) == True
assert move_one_ball([1]) == True
assert move_one_ball([1, 2, 3]) == True
assert move_one_ball([3, 4, 5, 1, 2]) == True
assert move_one_ball([3, 5, 4, 1, 2]) == False
assert move_one_ball([1, 3, 2]) == False
assert move_one_ball([2, 3, 1]) == True
assert move_one_ball([4, 1, 3, 2]) == False
