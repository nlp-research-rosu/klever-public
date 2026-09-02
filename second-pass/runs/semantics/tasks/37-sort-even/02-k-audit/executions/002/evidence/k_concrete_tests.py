def sort_even(l: list):
    evens = sorted(l[::2])
    odds = l[1::2]
    result = []
    i = 0
    odd = 0
    for odd in odds:
        result.append(evens[i])
        result.append(odd)
        i += 1
    return result + evens[len(odds):]


# Loop-zero and suffix-zero/one boundaries, prompt examples, duplicates,
# negatives, already-sorted, and reverse-sorted even subsequences.
assert sort_even([]) == []
assert sort_even([7]) == [7]
assert sort_even([1, 2]) == [1, 2]
assert sort_even([1, 2, 3]) == [1, 2, 3]
assert sort_even([5, 6, 3, 4]) == [3, 6, 5, 4]
assert sort_even([9, -1, 3, -2, 3, -3, 0]) == [0, -1, 3, -2, 3, -3, 9]
assert sort_even([4, 10, 3, 11, 2, 12, 1, 13]) == [1, 10, 2, 11, 3, 12, 4, 13]
assert sort_even([-2, 8, -2, 7, -3, 6]) == [-3, 8, -2, 7, -2, 6]
