def find_max(words):
    best = ""
    max_unique = 0
    word = ""
    unique = 0
    for word in words:
        unique = len(set(word))
        if unique > max_unique:
            best = word
            max_unique = unique
        elif unique == max_unique:
            if word < best:
                best = word
    return best
