def search(lst):
    answer = -1
    candidate = 1
    frequency = 0
    item = 1
    for candidate in lst:
        frequency = 0
        for item in lst:
            if item == candidate:
                frequency = frequency + 1
        if frequency >= candidate:
            if candidate > answer:
                answer = candidate + 0
    return answer
