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
assert specialFilter([9, 10, 11, 12, 19, 20, 21, 22, 31, 32, 99, 100, 101, 109]) == 6
assert specialFilter([10**100 + 1, 3 * 10**120 + 9, 8 * 10**80 + 7]) == 2
