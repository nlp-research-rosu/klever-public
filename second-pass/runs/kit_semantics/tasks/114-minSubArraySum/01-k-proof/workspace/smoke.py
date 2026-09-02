def minSubArraySum(nums):
    current = 0
    minimum = nums[0]
    for value in nums:
        current = min(value, current + value)
        minimum = min(minimum, current)
    return minimum


assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
assert minSubArraySum([-1, -2, -3]) == -6
assert minSubArraySum([5]) == 5
assert minSubArraySum([3, -4, 2, -3, -1, 7, -5]) == -6
assert minSubArraySum([0, 0]) == 0
