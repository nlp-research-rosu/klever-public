def search(lst):
    answer = -1
    for value in lst:
        if lst.count(value) >= value:
            if value > answer:
                answer = value
    return answer
