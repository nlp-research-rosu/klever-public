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


assert order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
assert order_by_points([]) == []
assert order_by_points([0, -10, 10, -1, 1]) == [-10, -1, 0, 10, 1]
assert order_by_points([100, 10, 1, -100, -10, -1]) == [-100, -10, -1, 100, 10, 1]
