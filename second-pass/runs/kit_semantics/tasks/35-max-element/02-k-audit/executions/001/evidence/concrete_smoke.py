def max_element(l: list):
    return max(l)


assert max_element([1, 2, 3]) == 3
assert max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]) == 123
assert max_element([-4]) == -4
assert max_element([1, 2]) == 2
assert max_element([2, 1]) == 2
assert max_element([2, 2, 1]) == 2
assert max_element([False, True, False]) == True
assert max_element([1, 2.5, True, -4]) == 2.5
assert max_element([1.5, -2, 3.25]) == 3.25
assert max_element([9007199254740993, 9007199254740992.0]) == 9007199254740993
assert max_element(["ant", "zebra", "yak"]) == "zebra"
