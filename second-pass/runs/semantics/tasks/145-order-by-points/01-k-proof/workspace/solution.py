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
