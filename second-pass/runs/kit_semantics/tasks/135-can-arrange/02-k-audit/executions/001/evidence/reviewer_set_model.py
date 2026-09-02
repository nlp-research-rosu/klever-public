def can_arrange(arr):
    index = -1
    i = 0
    previous = 0
    value = 0
    for value in arr:
        if i > 0:
            if not value >= previous:
                index = i
        previous = value
        i = i + 1
    return index


assert can_arrange([set("a"), set("b")]) == 1
