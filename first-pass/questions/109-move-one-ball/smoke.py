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


# HumanEval/109 dataset `check` cases (bare-bool asserts).
assert move_one_ball([3, 4, 5, 1, 2])
assert move_one_ball([3, 5, 10, 1, 2])
assert not move_one_ball([4, 3, 1, 2])
assert not move_one_ball([3, 5, 4, 1, 2])
assert move_one_ball([])
