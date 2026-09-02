def sort_even(l: list):
    result = list(l)
    evens = sorted(l[::2])
    i = 0
    for i in range((len(l) + 1) // 2):
        result[2 * i] = evens[i]
    return result


assert sort_even([]) == []
assert sort_even([7]) == [7]
assert sort_even([1, 2, 3]) == [1, 2, 3]
assert sort_even([5, 6, 3, 4]) == [3, 6, 5, 4]
assert sort_even([9, -1, 4, -2, 4]) == [4, -1, 4, -2, 9]
