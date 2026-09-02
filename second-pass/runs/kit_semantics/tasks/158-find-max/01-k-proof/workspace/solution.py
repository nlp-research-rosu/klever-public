def find_max(words):
    result = ""
    max_unique = -1
    word = ""
    unique = -1
    for word in words:
        unique = len(set(word))
        if unique > max_unique or unique == max_unique and word < result:
            result = word
            max_unique = unique
    return result
