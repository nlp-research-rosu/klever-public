def is_nested(string):
    num_opens = 0
    num_closes = 0
    first_open = -1
    second_open = -1
    last_close = -1
    second_last_close = -1
    i = 0
    for i in range(len(string)):
        if string[i] == '[':
            num_opens = num_opens + 1
            if num_opens == 1:
                first_open = i
            if num_opens == 2:
                second_open = i
        else:
            num_closes = num_closes + 1
            second_last_close = last_close
            last_close = i
    return num_opens >= 2 and num_closes >= 2 and first_open < last_close and second_open < second_last_close
