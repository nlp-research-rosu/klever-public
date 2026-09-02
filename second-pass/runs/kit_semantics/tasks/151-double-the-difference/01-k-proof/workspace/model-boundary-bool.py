def double_the_difference(lst):
    result = 0
    number = 0
    for number in lst:
        if isinstance(number, int):
            if number > 0:
                if number % 2 == 1:
                    result += number * number
    return result


# The supplied K model's isIntV treats Bool as disjoint from Int.
assert double_the_difference([True]) == 0
