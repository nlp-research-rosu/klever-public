def specialFilter(nums):
    count = 0
    num = 0
    text = ""
    for num in nums:
        if num > 10:
            text = str(num)
            if ord(text[0]) % 2 == 1:
                if ord(text[-1]) % 2 == 1:
                    count += 1
    return count


assert specialFilter([15, -73, 14, -15]) == 1
assert specialFilter([33, -2, -3, 45, 21, 109]) == 2
assert specialFilter([]) == 0
