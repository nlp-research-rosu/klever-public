def search(lst):
    result = -1
    for value in lst:
        count = 0
        for item in lst:
            if item == value:
                count += 1
        if count >= value:
            if value > result:
                result = value
    return result
