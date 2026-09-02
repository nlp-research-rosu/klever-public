def double_the_difference(lst):
    total = 0
    number = 0
    for number in lst:
        if isinstance(number, int) and number > 0 and number % 2 == 1:
            total += number ** 2
    return total


assert double_the_difference([1, 3, 2, 0]) == 10
assert double_the_difference([-1, -2, 0]) == 0
assert double_the_difference([9, -2]) == 81
assert double_the_difference([0]) == 0
assert double_the_difference([]) == 0
assert double_the_difference([3.0, 3, -5, 2.5, 7]) == 58
