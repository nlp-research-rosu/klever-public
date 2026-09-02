def specialFilter(nums):
    count = 0
    for num in nums:
        if num > 10:
            first = num
            while first >= 10:
                first = first // 10
            if first % 2 == 1:
                if num % 2 == 1:
                    count += 1
    return count
