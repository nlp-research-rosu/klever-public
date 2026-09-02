def digit_sum(num):
    if num < -9:
        return (-num) % 10 + digit_sum(-((-num) // 10))
    else:
        if num > 9:
            return num % 10 + digit_sum(num // 10)
        else:
            return num


def count_nums(arr):
    if arr == []:
        return 0
    else:
        if digit_sum(arr[0]) > 0:
            return 1 + count_nums(arr[1:])
        else:
            return count_nums(arr[1:])
