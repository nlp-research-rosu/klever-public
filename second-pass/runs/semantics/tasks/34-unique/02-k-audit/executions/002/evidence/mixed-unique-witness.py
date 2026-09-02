def unique(l: list):
    result = []
    for item in l:
        if item not in result:
            result.append(item)
    return sorted(result)


assert unique([1, True]) == [1]
