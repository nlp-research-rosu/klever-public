def skjkasdkd(lst):
    largest = 0
    value = 0
    candidate = False
    divisor = 2
    for value in lst:
        if value > largest:
            candidate = value >= 2
            divisor = 2
            while divisor < value:
                if value % divisor == 0:
                    candidate = False
                divisor += 1
            if candidate:
                largest = value + 0
    total = 0
    while largest > 0:
        total += largest % 10
        largest //= 10
    return total


assert skjkasdkd(
    [0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3]
) == 10
assert skjkasdkd([1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1]) == 25
assert skjkasdkd([1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3]) == 13
assert skjkasdkd([0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6]) == 11
assert skjkasdkd([0, 81, 12, 3, 1, 21]) == 3
assert skjkasdkd([0, 8, 1, 2, 1, 7]) == 7
assert skjkasdkd([]) == 0
assert skjkasdkd([-7, -3, 0, 1, 4]) == 0
