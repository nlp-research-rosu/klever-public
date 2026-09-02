def double_the_difference(lst):
    result = 0
    number = 0
    for number in lst:
        if isinstance(number, int):
            if number > 0:
                if number % 2 == 1:
                    result += number * number
    return result


assert double_the_difference([]) == 0
assert double_the_difference([1, 3, 2, 0]) == 10
assert double_the_difference([-3, -2, -1, 0, 1, 2, 3]) == 10
assert double_the_difference([-1, -2, 0]) == 0
assert double_the_difference([9, -2]) == 81
assert double_the_difference([0]) == 0
assert double_the_difference([1.5, 3, -5, 7.0, 5]) == 34
assert double_the_difference([1000000000000000000001]) == 1000000000000000000002000000000000000000001
