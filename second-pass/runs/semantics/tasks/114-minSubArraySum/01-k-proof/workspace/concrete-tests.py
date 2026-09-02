def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty
    sub-array of nums.
    """
    smallest = nums[0]
    current = 0
    value = 0
    for value in nums:
        current = current + value
        if value < current:
            current = value
        if current < smallest:
            smallest = current
    return smallest


assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
assert minSubArraySum([-1, -2, -3]) == -6
assert minSubArraySum([5]) == 5
assert minSubArraySum([3, -4, 2, -3, -1, 7, -5]) == -6
assert minSubArraySum([0, 0]) == 0
