def digit_sum(number):
    if number < 0:
        sign = -1
        number = -number
    else:
        sign = 1
    total = 0
    while number >= 10:
        total += number % 10
        number //= 10
    return total + sign * number


def order_by_points(nums):
    return sorted(nums, key=digit_sum)
