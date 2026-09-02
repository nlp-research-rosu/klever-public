def double_the_difference(lst):
    total = 0
    number = 0
    for number in lst:
        if isinstance(number, int) and number > 0 and number % 2 == 1:
            total += number ** 2
    return total
