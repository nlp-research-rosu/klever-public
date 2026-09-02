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
assert specialFilter([12]) == 0
assert specialFilter([15]) == 1
assert specialFilter([12, 15, 33]) == 2
assert specialFilter([15, -73, 14, -15]) == 1
assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
