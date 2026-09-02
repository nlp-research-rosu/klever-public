def sorted_list_sum(lst):
    result = []
    word = ""
    for word in lst:
        if len(word) % 2 == 0:
            result.append(word)
    return sorted(sorted(result), key=len)
