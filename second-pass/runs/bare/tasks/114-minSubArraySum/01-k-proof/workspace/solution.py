def min_prefix_sum(nums):
    if len(nums) == 1:
        return nums[0]
    tail_min = min_prefix_sum(nums[1:])
    return min(nums[0], nums[0] + tail_min)


def minSubArraySum(nums):
    if len(nums) == 1:
        return nums[0]
    tail_min = minSubArraySum(nums[1:])
    prefix_min = min_prefix_sum(nums)
    return min(tail_min, prefix_min)
