def remove_duplicates(numbers):
    result = []
    m = len(numbers)
    i = 0
    j = 0
    c = 0
    for i in range(0, m):
        c = 0
        for j in range(0, m):
            if numbers[j] == numbers[i]:
                c = c + 1
        if c == 1:
            result = result + [numbers[i]]
    return result
