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
