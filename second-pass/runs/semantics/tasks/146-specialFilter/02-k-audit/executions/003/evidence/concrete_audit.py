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


assert specialFilter([]) == 0
assert specialFilter([10]) == 0
assert specialFilter([11]) == 1
assert specialFilter([12]) == 0
assert specialFilter([20, 21, 31, 99, 100, 101, 109]) == 4
assert specialFilter([15, -73, 14, -15]) == 1
assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
assert specialFilter([-999, 0, 9, 10, 24681, 13579, 9990]) == 1
