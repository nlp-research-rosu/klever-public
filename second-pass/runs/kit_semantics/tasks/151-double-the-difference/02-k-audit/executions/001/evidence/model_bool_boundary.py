def double_the_difference(lst):
    result = 0
    number = 0
    for number in lst:
        if isinstance(number, int):
            if number > 0:
                if number % 2 == 1:
                    result += number * number
    return result


# This is true under the supplied MPY model because Bool is not an Int subsort.
assert double_the_difference([True]) == 0
