def sort_array(array):
    if not array:
        return []
    if (array[0] + array[-1]) % 2 == 1:
        return sorted(array)
    return sorted(array, reverse=True)


assert sort_array([]) == []
assert sort_array([5]) == [5]
assert sort_array([2, 4, 3, 0, 1, 5]) == [0, 1, 2, 3, 4, 5]
assert sort_array([2, 4, 3, 0, 1, 5, 6]) == [6, 5, 4, 3, 2, 1, 0]

original = [2, 4, 3, 0, 1, 5]
result = sort_array(original)
assert original == [2, 4, 3, 0, 1, 5]
assert result == [0, 1, 2, 3, 4, 5]
