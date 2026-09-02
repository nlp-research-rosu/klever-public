def minSubArraySum(nums):
    current = 0
    minimum = nums[0]
    for value in nums:
        current = min(value, current + value)
        minimum = min(minimum, current)
    return minimum
