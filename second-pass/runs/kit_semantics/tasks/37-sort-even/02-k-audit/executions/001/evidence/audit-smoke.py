def sort_even(l: list):
    result = list(l)
    evens = sorted(l[::2])
    i = 0
    for i in range((len(l) + 1) // 2):
        result[2 * i] = evens[i]
    return result


assert sort_even([]) == []
assert sort_even([7]) == [7]
assert sort_even([2, 1]) == [2, 1]
assert sort_even([9, 8, 3]) == [3, 8, 9]
assert sort_even([5, 6, 3, 4]) == [3, 6, 5, 4]
assert sort_even([5, -9, -1, 8, 0]) == [-1, -9, 0, 8, 5]
