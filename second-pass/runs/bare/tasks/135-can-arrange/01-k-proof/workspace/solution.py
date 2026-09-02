def can_arrange(arr):
    if len(arr) <= 1:
        return -1
    else:
        result = can_arrange(arr[1:])
        if result != -1:
            return result + 1
        else:
            if arr[1] < arr[0]:
                return 1
            else:
                return -1
