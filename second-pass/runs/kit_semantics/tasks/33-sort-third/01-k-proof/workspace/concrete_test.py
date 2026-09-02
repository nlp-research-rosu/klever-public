def sort_third(l: list):
    thirds = sorted(l[::3])
    result = []
    i = 0
    while i < len(l):
        if i % 3 == 0:
            result.append(thirds[i // 3])
        else:
            result.append(l[i])
        i += 1
    return result


assert sort_third([]) == []
assert sort_third([1]) == [1]
assert sort_third([1, 2, 3]) == [1, 2, 3]
assert sort_third([5, 6, 3, 4, 8, 9, 2]) == [2, 6, 3, 4, 8, 9, 5]
assert sort_third([9, 1, 2, 4]) == [4, 1, 2, 9]
assert sort_third([8, -1, 7, 6, 5, 4, 3, 2, 1, 0]) == [
    0, -1, 7, 3, 5, 4, 6, 2, 1, 8
]
assert sort_third(["z", "keep", "also", "a"]) == [
    "a", "keep", "also", "z"
]
