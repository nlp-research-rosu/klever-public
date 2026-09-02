def common(l1: list, l2: list):
    result = []
    item = 0
    for item in l1:
        if item in l2 and item not in result:
            result.append(item)
    return sorted(result)
