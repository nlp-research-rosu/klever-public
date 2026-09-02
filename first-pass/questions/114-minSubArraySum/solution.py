def minSubArraySum(nums):
    cur = nums[0]
    best = nums[0]
    first = True
    x = 0
    for x in nums:
        if first:
            first = False
        else:
            if x < cur + x:
                cur = x
            else:
                cur = cur + x
            if cur < best:
                best = cur
    return best
