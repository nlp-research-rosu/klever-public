def solve(N):
    digit_sum = N % 10
    N = N // 10
    digit_sum += N % 10
    N = N // 10
    digit_sum += N % 10
    N = N // 10
    digit_sum += N % 10
    N = N // 10
    digit_sum += N % 10

    if digit_sum < 8:
        if digit_sum == 0:
            return "0"
        elif digit_sum == 1:
            return "1"
        elif digit_sum == 2:
            return "10"
        elif digit_sum == 3:
            return "11"
        elif digit_sum == 4:
            return "100"
        elif digit_sum == 5:
            return "101"
        elif digit_sum == 6:
            return "110"
        else:
            return "111"
    elif digit_sum < 16:
        if digit_sum == 8:
            return "1000"
        elif digit_sum == 9:
            return "1001"
        elif digit_sum == 10:
            return "1010"
        elif digit_sum == 11:
            return "1011"
        elif digit_sum == 12:
            return "1100"
        elif digit_sum == 13:
            return "1101"
        elif digit_sum == 14:
            return "1110"
        else:
            return "1111"
    elif digit_sum < 24:
        if digit_sum == 16:
            return "10000"
        elif digit_sum == 17:
            return "10001"
        elif digit_sum == 18:
            return "10010"
        elif digit_sum == 19:
            return "10011"
        elif digit_sum == 20:
            return "10100"
        elif digit_sum == 21:
            return "10101"
        elif digit_sum == 22:
            return "10110"
        else:
            return "10111"
    elif digit_sum < 32:
        if digit_sum == 24:
            return "11000"
        elif digit_sum == 25:
            return "11001"
        elif digit_sum == 26:
            return "11010"
        elif digit_sum == 27:
            return "11011"
        elif digit_sum == 28:
            return "11100"
        elif digit_sum == 29:
            return "11101"
        elif digit_sum == 30:
            return "11110"
        else:
            return "11111"
    else:
        if digit_sum == 32:
            return "100000"
        elif digit_sum == 33:
            return "100001"
        elif digit_sum == 34:
            return "100010"
        elif digit_sum == 35:
            return "100011"
        else:
            return "100100"
