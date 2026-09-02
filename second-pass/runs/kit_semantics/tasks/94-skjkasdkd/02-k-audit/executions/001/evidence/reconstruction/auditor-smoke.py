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


assert skjkasdkd([]) == 0
assert skjkasdkd([-9, -1, 0, 1, 4, 49]) == 0
assert skjkasdkd([2]) == 2
assert skjkasdkd([4, 3, 2]) == 3
assert skjkasdkd([181, 179, 180]) == 10
assert skjkasdkd([1, 0, 1, 8, 2, 4597, 40, 5]) == 25
