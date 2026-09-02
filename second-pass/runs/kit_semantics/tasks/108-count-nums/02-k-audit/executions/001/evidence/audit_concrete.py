def count_nums(arr):
    count = 0
    for num in arr:
        if num < 0:
            n = -num
        else:
            n = num

        digit_sum = 0
        first_digit = 0
        char = "0"
        digit = 0
        for char in str(n):
            digit = int(char)
            if first_digit == 0:
                first_digit = digit
            digit_sum += digit

        if num < 0:
            digit_sum -= 2 * first_digit

        if digit_sum > 0:
            count += 1

    return count


assert count_nums([]) == 0
assert count_nums([-1, 11, -11]) == 1
assert count_nums([1, 1, 2]) == 3
assert count_nums([0, -11, -12, -99, -109, 10, 101]) == 4
assert count_nums([-100, -101, -102, -999, 999]) == 3
