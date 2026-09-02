def pluck(arr):
    smallest = -1
    smallest_index = 0
    index = 0
    value = 0

    for value in arr:
        value = value + 0
        if value % 2 == 0:
            if smallest < 0:
                smallest = value
                smallest_index = index
            else:
                if value < smallest:
                    smallest = value
                    smallest_index = index
        index += 1

    if smallest < 0:
        return []
    return [smallest, smallest_index]


assert pluck([4, 2, 3]) == [2, 1]
assert pluck([1, 2, 3]) == [2, 1]
assert pluck([]) == []
assert pluck([5, 0, 3, 0, 4, 2]) == [0, 1]
assert pluck([2, 2]) == [2, 0]
assert pluck([1, 3, 5]) == []
