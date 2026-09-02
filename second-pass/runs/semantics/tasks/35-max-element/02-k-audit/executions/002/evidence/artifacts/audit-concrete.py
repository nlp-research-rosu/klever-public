def max_element(l: list):
    return max(l)


assert max_element([1, 2, 3]) == 3
assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == 123
assert max_element([-7]) == -7
assert max_element([-9, -2, -14, -2]) == -2
assert max_element([0, 1, 0]) == 1
