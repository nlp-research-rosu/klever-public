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
