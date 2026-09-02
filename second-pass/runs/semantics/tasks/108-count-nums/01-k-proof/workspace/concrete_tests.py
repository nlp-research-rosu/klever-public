def positive_digit_sum(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


def negative_digit_sum(n):
    total = 0
    while n >= 10:
        total += n % 10
        n //= 10
    return total - n


def signed_digit_sum(n):
    if n < 0:
        return negative_digit_sum(0 - n)
    return positive_digit_sum(n)


def count_nums(arr):
    count = 0
    for n in arr:
        if signed_digit_sum(n) > 0:
            count += 1
    return count


assert count_nums([]) == 0
assert count_nums([-1, 11, -11]) == 1
assert count_nums([1, 1, 2]) == 3
assert count_nums([0, 10, -10, 123, -123]) == 3
assert count_nums([-12, -21, -123, -999, 100, -100]) == 4
