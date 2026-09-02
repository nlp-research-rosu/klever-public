def pluck(arr):
    i = 0
    found = False
    bestVal = 0
    bestIdx = 0
    v = 0
    for v in arr:
        if v % 2 == 0:
            if not found:
                bestVal = v
                bestIdx = i
                found = True
            else:
                if v < bestVal:
                    bestVal = v
                    bestIdx = i
        i = i + 1
    if found:
        return [bestVal, bestIdx]
    else:
        return []


# HumanEval/68 dataset `check` cases.
assert pluck([4, 2, 3]) == [2, 1]
assert pluck([1, 2, 3]) == [2, 1]
assert pluck([]) == []
assert pluck([5, 0, 3, 0, 4, 2]) == [0, 1]
assert pluck([1, 2, 3, 0, 5, 3]) == [0, 3]
assert pluck([5, 4, 8, 4, 8]) == [4, 1]
assert pluck([7, 6, 7, 1]) == [6, 1]
assert pluck([7, 9, 7, 1]) == []
