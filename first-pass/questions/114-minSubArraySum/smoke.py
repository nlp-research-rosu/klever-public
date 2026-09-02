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


# Smoke checks from the prompt docstring (NOT hidden tests).
assert minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
assert minSubArraySum([-1, -2, -3]) == -6
assert minSubArraySum([-1, -2, -3, 2, -10]) == -14
assert minSubArraySum([0, 10, 20, 1000000]) == 0
