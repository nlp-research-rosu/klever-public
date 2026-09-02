def specialFilter(nums):
    count = 0
    num = 0
    digits = ""
    for num in nums:
        if num > 10:
            digits = str(num)
            if digits[0] in "13579" and digits[-1] in "13579":
                count += 1
    return count
