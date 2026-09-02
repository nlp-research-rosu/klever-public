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


assert specialFilter([15, -73, 14, -15]) == 1
assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
assert specialFilter([]) == 0
assert specialFilter([11, 13, 22, 31, 79, 109, 111, 13579, 20, 9990]) == 7
assert specialFilter([10, -11, 12, 20, 101, 123, 333, 707]) == 4
