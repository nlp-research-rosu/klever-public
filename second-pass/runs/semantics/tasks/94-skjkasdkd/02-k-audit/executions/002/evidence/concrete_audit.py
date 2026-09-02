def skjkasdkd(lst):
    largest = 0
    number = 0
    divisor = 2
    prime = False
    digit_total = 0
    for number in lst:
        if number > largest:
            divisor = 2
            prime = number >= 2
            while prime and divisor * divisor <= number:
                if number % divisor == 0:
                    prime = False
                divisor += 1
            if prime:
                largest = number
    while largest > 0:
        digit_total += largest % 10
        largest //= 10
    return digit_total


assert skjkasdkd([]) == 0
assert skjkasdkd([1]) == 0
assert skjkasdkd([2]) == 2
assert skjkasdkd([4]) == 0
assert skjkasdkd([-5, 0, 1, 9, 25]) == 0
assert skjkasdkd([97, 101, 99]) == 2
assert skjkasdkd([0, 3, 2, 1, 181, 324]) == 10
