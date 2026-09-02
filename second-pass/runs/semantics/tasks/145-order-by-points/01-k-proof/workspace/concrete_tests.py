def digit_sum(n):
    negative = n < 0
    n = abs(n)
    total = 0
    most_significant = 0
    while n:
        most_significant = n % 10
        total += most_significant
        n //= 10
    if negative:
        total -= 2 * most_significant
    return total


def order_by_points(nums):
    return sorted(nums, key=digit_sum)


assert order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
assert order_by_points([]) == []
assert order_by_points([0, -10, 100, 2, -2, 20]) == [-2, -10, 0, 100, 2, 20]
assert order_by_points([99, -123, 8, 80, -9]) == [-9, -123, 8, 80, 99]
